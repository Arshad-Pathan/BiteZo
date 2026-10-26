from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Restaurant(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="restaurants/", blank=True, null=True)
    delivery_time = models.CharField(max_length=50, default="30-40 min")
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        ratings = self.reviews.aggregate(average=models.Avg("rating"))
        return ratings["average"] or 0


class RestaurantPhoto(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to="restaurant_photos/")
    caption = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Photo for {self.restaurant.name}"


class RestaurantOffer(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="offers"
    )
    title = models.CharField(max_length=120)
    code = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    terms = models.CharField(max_length=255, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["valid_until", "title"]

    def __str__(self):
        return f"{self.restaurant.name}: {self.title}"


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restaurant_reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["restaurant", "user"], name="unique_restaurant_review"
            ),
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.rating}/5"


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    DIETARY_CHOICES = [
        ("veg", "Vegetarian"),
        ("non_veg", "Non-vegetarian"),
        ("unknown", "Not specified"),
    ]
    restaurant = models.CharField(max_length=1000)
    restaurant_ref = models.ForeignKey(
        Restaurant, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="products",
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="products",
    )
    dietary_type = models.CharField(
        max_length=10, choices=DIETARY_CHOICES, default="unknown"
    )
    name = models.CharField(max_length=1000)

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    is_available = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="food_favorites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_food_favorite"),
        ]
