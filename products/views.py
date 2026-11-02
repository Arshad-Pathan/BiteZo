from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.utils import timezone
from .models import (
    Product, Restaurant, Category, Favorite, RestaurantOffer,
    RestaurantReview,
)
from food_delivery.decorator import *


def home(request):
    active_tab = request.GET.get("tab", "delivery")
    if active_tab != "gharkakhana":
        active_tab = "delivery"

    context = {"active_tab": active_tab}

    if active_tab == "gharkakhana":
        context["cloud_kitchens"] = Restaurant.objects.filter(
            is_active=True, is_cloud_kitchen=True
        ).annotate(
            menu_item_count=Count("products", filter=Q(products__is_available=True)),
            rating_average=Avg("reviews__rating"),
            review_count=Count("reviews", distinct=True),
        )
        return render(request, "home.html", context)

    products = Product.objects.select_related("restaurant_ref", "category").all()
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    restaurant = request.GET.get("restaurant", "")
    dietary_type = request.GET.get("dietary_type", "")
    availability = request.GET.get("availability", "available")

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(restaurant__icontains=query) |
            Q(restaurant_ref__name__icontains=query)
        )
    if category:
        products = products.filter(category__slug=category)
    if restaurant:
        products = products.filter(restaurant_ref_id=restaurant)
    if dietary_type in {"veg", "non_veg", "unknown"}:
        products = products.filter(dietary_type=dietary_type)
    if availability == "available":
        products = products.filter(is_available=True)
    elif availability == "unavailable":
        products = products.filter(is_available=False)

    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list("product_id", flat=True)
        )
    context.update({
        "products": products,
        "categories": Category.objects.all(),
        "restaurants": Restaurant.objects.filter(is_active=True),
        "favorite_ids": favorite_ids,
    })
    return render(request, "home.html", context)


def restaurant_list(request):
    restaurants = Restaurant.objects.filter(is_active=True).annotate(
        menu_item_count=Count("products", filter=Q(products__is_available=True)),
        rating_average=Avg("reviews__rating"),
        review_count=Count("reviews", distinct=True),
    )
    return render(request, "products/restaurant_list.html", {"restaurants": restaurants})


def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id, is_active=True)
    products = restaurant.products.filter(is_available=True).select_related("category")
    active_offers = restaurant.offers.filter(is_active=True).filter(
        Q(valid_until__isnull=True) | Q(valid_until__gte=timezone.localdate())
    )
    reviews = restaurant.reviews.select_related("user")
    rating_summary = reviews.aggregate(average=Avg("rating"), count=Count("id"))
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    return render(request, "products/restaurant_detail.html", {
        "restaurant": restaurant,
        "products": products,
        "photos": restaurant.photos.all(),
        "offers": active_offers,
        "reviews": reviews,
        "rating_average": rating_summary["average"] or 0,
        "review_count": rating_summary["count"],
        "user_review": user_review,
    })


@login_required
def restaurant_review(request, id):
    if request.method != "POST":
        return redirect("restaurant_detail", id=id)

    restaurant = get_object_or_404(Restaurant, id=id, is_active=True)
    try:
        rating = int(request.POST.get("rating", 0))
    except (TypeError, ValueError):
        rating = 0
    comment = request.POST.get("comment", "").strip()

    if rating not in range(1, 6):
        messages.error(request, "Please choose a rating from 1 to 5 stars.")
        return redirect("restaurant_detail", id=restaurant.id)
    if len(comment) > 1000:
        messages.error(request, "Your review must be 1,000 characters or fewer.")
        return redirect("restaurant_detail", id=restaurant.id)

    review, created = RestaurantReview.objects.update_or_create(
        restaurant=restaurant,
        user=request.user,
        defaults={"rating": rating, "comment": comment},
    )
    messages.success(
        request,
        "Thanks for sharing your review." if created else "Your review has been updated.",
    )
    return redirect("restaurant_detail", id=restaurant.id)


def product_detail(request, id):
    product = get_object_or_404(Product.objects.select_related("restaurant_ref", "category"), id=id)
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(
        user=request.user, product=product
    ).exists()
    return render(request, "products/product_detail.html", {
        "product": product, "is_favorite": is_favorite,
    })


@login_required
def favorite_toggle(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            favorite.delete()
    return redirect(request.POST.get("next") or "home")


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related(
        "product", "product__restaurant_ref"
    )
    return render(request, "products/favorite_list.html", {"favorites": favorites})




# READ
@superuser_required
def product_list(request):
    products = Product.objects.all()

    return render(
        request,
        "products/product_list.html",
        {"products": products}
    )


# CREATE
@superuser_required
def product_create(request):

    if request.method == "POST":

        restaurant = request.POST.get("restaurant")
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        restaurant_ref = get_object_or_404(Restaurant, id=request.POST.get("restaurant_ref"))
        category = get_object_or_404(Category, id=request.POST.get("category"))

        Product.objects.create(
            restaurant=restaurant_ref.name,
            restaurant_ref=restaurant_ref,
            category=category,
            dietary_type=request.POST.get("dietary_type", "unknown"),
            name=name,
            description=description,
            price=price,
            image=image
        )

        return redirect("product_list")

    return render(request, "products/product_form.html", {
        "restaurants": Restaurant.objects.filter(is_active=True),
        "categories": Category.objects.all(),
        "dietary_choices": Product.DIETARY_CHOICES,
    })




# UPDATE
@superuser_required
def product_update(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == "POST":
        restaurant_ref = get_object_or_404(Restaurant, id=request.POST.get("restaurant_ref"))
        product.restaurant = restaurant_ref.name
        product.restaurant_ref = restaurant_ref
        product.category = get_object_or_404(Category, id=request.POST.get("category"))
        product.dietary_type = request.POST.get("dietary_type", "unknown")
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.is_available = (
            request.POST.get("is_available") == "on"
        )

        product.save()

        return redirect("product_list")

    return render(
        request,
        "products/product_form.html",
        {
            "product": product,
            "restaurants": Restaurant.objects.filter(is_active=True),
            "categories": Category.objects.all(),
            "dietary_choices": Product.DIETARY_CHOICES,
        }
    )


# DELETE
@superuser_required
def product_delete(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == "POST":

        product.delete()

        return redirect("product_list")

    return render(
        request,
        "products/product_confirm_delete.html",
        {"product": product}
    )
