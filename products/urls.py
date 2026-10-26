from django.urls import path
from . import views

urlpatterns = [
    path("restaurants/", views.restaurant_list, name="restaurant_list"),
    path("restaurants/<int:id>/", views.restaurant_detail, name="restaurant_detail"),
    path("restaurants/<int:id>/review/", views.restaurant_review, name="restaurant_review"),
    path("food/<int:id>/", views.product_detail, name="product_detail"),
    path("food/<int:id>/favorite/", views.favorite_toggle, name="favorite_toggle"),
    path("favorites/", views.favorite_list, name="favorite_list"),
    
    path(
        "list/",
        views.product_list,
        name="product_list"
    ),

    path(
        "create/",
        views.product_create,
        name="product_create"
    ),

    path(
        "update/<int:id>/",
        views.product_update,
        name="product_update"
    ),

    path(
        "delete/<int:id>/",
        views.product_delete,
        name="product_delete"
    ),
]

