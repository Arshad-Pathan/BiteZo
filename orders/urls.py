from django.urls import path
from . import views


urlpatterns = [

    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/", views.cart_add, name="cart_add"),
    path("cart/update/", views.cart_update, name="cart_update"),
    path("cart/clear/", views.cart_clear, name="cart_clear"),
    path("cart/checkout/", views.cart_checkout, name="cart_checkout"),

    path(
        "",
        views.order_list,
        name="order_list"
    ),

    path(
        "create/",
        views.order_create,
        name="order_create"
    ),

    path(
        "<int:id>/",
        views.order_detail,
        name="order_detail"
    ),

    path(
        "<int:id>/update/",
        views.order_update,
        name="order_update"
    ),

    path(
        "<int:id>/delete/",
        views.order_delete,
        name="order_delete"
    ),
]
