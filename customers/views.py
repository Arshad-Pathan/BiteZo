
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Customer
from food_delivery.decorator import superuser_required

# CREATE
def customer_create(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        Customer.objects.create(
            user=user,
            phone=phone,
            address=address
        )

        return redirect("login")

    return render(request, "customers/customer_form.html")


# READ
@superuser_required
def customer_list(request):

    customers = Customer.objects.all()

    return render(
        request,
        "customers/customer_list.html",
        {"customers": customers}
    )


# UPDATE
def customer_update(request, id):

    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":

        customer.user.username = request.POST.get("username")
        customer.user.save()

        customer.phone = request.POST.get("phone")
        customer.address = request.POST.get("address")

        customer.save()

        return redirect("customer_list")

    return render(
        request,
        "customers/customer_form.html",
        {"customer": customer}
    )


# DELETE
def customer_delete(request, id):

    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":
        customer.user.delete()

        return redirect("customer_list")

    return render(
        request,
        "customers/customer_confirm_delete.html",
        {"customer": customer}
    )
