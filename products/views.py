from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from food_delivery.decorator import *


def home(request):
    products = Product.objects.all()
    return render(request, "home.html", {"products":products})




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

        Product.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            image=image
        )

        return redirect("product_list")

    return render(
        request,
        "products/product_form.html"
    )




# UPDATE
@superuser_required
def product_update(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == "POST":
        product.restaurant = request.POST.get("restaurant")
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
        {"product": product}
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