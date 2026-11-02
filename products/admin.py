from django.contrib import admin
from .models import (
    Product, Restaurant, CloudKitchen, Category, Favorite, RestaurantPhoto,
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
    list_display = ("name", "phone", "opening_time", "closing_time", "is_active", "is_cloud_kitchen")
    list_filter = ("is_active", "is_cloud_kitchen")
    search_fields = ("name", "address", "phone")
    inlines = (RestaurantPhotoInline, RestaurantOfferInline)


@admin.register(CloudKitchen)
class CloudKitchenAdmin(RestaurantAdmin):
    list_display = ("name", "phone", "opening_time", "closing_time", "is_active")
    list_filter = ("is_active",)
    exclude = ("is_cloud_kitchen",)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_cloud_kitchen=True)

    def save_model(self, request, obj, form, change):
        obj.is_cloud_kitchen = True
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
admin.site.register(Favorite)
admin.site.register(RestaurantReview)
