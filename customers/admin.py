from django.contrib import admin
from .models import Customer, DeliveryAddress


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id","user","phone")


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ("label", "customer", "city", "is_default")
    list_filter = ("is_default", "city")
