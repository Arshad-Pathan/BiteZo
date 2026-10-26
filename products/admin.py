from django.contrib import admin
from .models import (
    Product, Restaurant, Category, Favorite, RestaurantPhoto,
    RestaurantOffer, RestaurantReview,
)

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
    )



class RestaurantPhotoInline(admin.TabularInline):
    model = RestaurantPhoto
    extra = 1


class RestaurantOfferInline(admin.TabularInline):
    model = RestaurantOffer
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "opening_time", "closing_time", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "address", "phone")
    inlines = (RestaurantPhotoInline, RestaurantOfferInline)


admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(RestaurantReview)
