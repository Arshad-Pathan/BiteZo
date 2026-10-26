from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0002_catalog_features"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="address",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="closing_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="opening_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="phone",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.CreateModel(
            name="RestaurantOffer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("code", models.CharField(blank=True, max_length=40)),
                ("description", models.TextField(blank=True)),
                ("terms", models.CharField(blank=True, max_length=255)),
                ("valid_until", models.DateField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("restaurant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="offers", to="products.restaurant")),
            ],
            options={"ordering": ["valid_until", "title"]},
        ),
        migrations.CreateModel(
            name="RestaurantPhoto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="restaurant_photos/")),
                ("caption", models.CharField(blank=True, max_length=150)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("restaurant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="photos", to="products.restaurant")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="RestaurantReview",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])),
                ("comment", models.TextField(blank=True, max_length=1000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("restaurant", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="products.restaurant")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="restaurant_reviews", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-updated_at"]},
        ),
        migrations.AddConstraint(
            model_name="restaurantreview",
            constraint=models.UniqueConstraint(fields=("restaurant", "user"), name="unique_restaurant_review"),
        ),
    ]
