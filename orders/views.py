from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from food_delivery.decorator import *
from django.contrib.auth.models import User
from .models import Order, OrderItem
from products.models import Product


# CREATE ORDER
@login_required
def order_create(request):
    if request.method == "POST":
        customer = request.user

        # Create order
        order = Order.objects.create(
            customer=customer,
            payment_successful=True
        )

        # Get products and quantities
        product_ids = request.POST.getlist("product")
        quantities = request.POST.getlist("quantity")

        for product_id, quantity in zip(
            product_ids,
            quantities
        ):

            if product_id and quantity:

                product = get_object_or_404(
                    Product,
                    id=product_id
                )

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=int(quantity)
                )

        return redirect(
            "order_detail",
            id=order.id
        )

    customers = User.objects.all()
    products = Product.objects.filter(
        is_available=True
    )

    return render(
        request,
        "orders/order_form.html",
        {
            "customers": customers,
            "products": products
        }
    )


# READ - ALL ORDERS
@login_required
def order_list(request):
    if request.user.is_superuser:
        orders = Order.objects.all().order_by("-created_at")
    else:
        orders = Order.objects.filter(customer=request.user).order_by("-created_at")

    return render(
        request,
        "orders/order_list.html",
        {
            "orders": orders
        }
    )


# READ - SINGLE ORDER
@login_required
def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order
        }
    )


# UPDATE ORDER
@login_required
def order_update(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    if request.method == "POST":
        order.customer = request.user
        order.save()

        # Remove old items
        order.items.all().delete()

        # Add updated items
        product_ids = request.POST.getlist(
            "product"
        )

        quantities = request.POST.getlist(
            "quantity"
        )

        for product_id, quantity in zip(
            product_ids,
            quantities
        ):

            if product_id and quantity:

                product = get_object_or_404(
                    Product,
                    id=product_id
                )

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=int(quantity)
                )

        return redirect(
            "order_detail",
            id=order.id
        )

    customers = User.objects.all()

    products = Product.objects.filter(
        is_available=True
    )

    return render(
        request,
        "orders/order_form.html",
        {
            "order": order,
            "customers": customers,
            "products": products
        }
    )


# DELETE ORDER
@login_required
def order_delete(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    if request.method == "POST":

        order.delete()

        return redirect(
            "order_list"
        )

    return render(
        request,
        "orders/order_confirm_delete.html",
        {
            "order": order
        }
    )

