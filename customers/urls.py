from django.urls import path
from . import views


urlpatterns = [

    path("", views.customer_list, name="customer_list"),

    path(
        "create/",
        views.customer_create,
        name="customer_create"
    ),

    path(
        "update/<int:id>/",
        views.customer_update,
        name="customer_update"
    ),

    path(
        "delete/<int:id>/",
        views.customer_delete,
        name="customer_delete"
    ),
]

