from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.text import slugify


def create_catalog_data(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Restaurant = apps.get_model("products", "Restaurant")
    Category = apps.get_model("products", "Category")
    category_names = [
        "Pizza", "Burgers", "Biryani", "Chinese", "Mexican",
        "Vegetarian", "South Indian", "Desserts", "Other",
    ]
    categories = {
        name: Category.objects.get_or_create(name=name, slug=slugify(name))[0]
        for name in category_names
    }
    keywords = {
        "pizza": "Pizza", "burger": "Burgers", "biryani": "Biryani",
        "noodle": "Chinese", "chinese": "Chinese", "mexican": "Mexican",
        "taco": "Mexican", "dosa": "South Indian", "idli": "South Indian",
        "dessert": "Desserts", "cake": "Desserts", "ice cream": "Desserts",
    }
    for product in Product.objects.all().iterator():
        restaurant_name = product.restaurant.strip() or "Unknown Restaurant"
        restaurant, _ = Restaurant.objects.get_or_create(name=restaurant_name)
        haystack = f"{product.name} {product.description}".lower()
        category_name = next(
            (value for key, value in keywords.items() if key in haystack), "Other"
        )
        product.restaurant_ref = restaurant
        product.category = categories[category_name]
        product.save(update_fields=["restaurant_ref", "category"])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("slug", models.SlugField(unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, unique=True)),
                ("description", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="restaurants/")),
                ("delivery_time", models.CharField(default="30-40 min", max_length=50)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="dietary_type",
            field=models.CharField(choices=[("veg", "Vegetarian"), ("non_veg", "Non-vegetarian"), ("unknown", "Not specified")], default="unknown", max_length=10),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="products", to="products.category"),
        ),
        migrations.AddField(
            model_name="product",
            name="restaurant_ref",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="products", to="products.restaurant"),
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorited_by", to="products.product")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="food_favorites", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(fields=("user", "product"), name="unique_food_favorite"),
        ),
        migrations.RunPython(create_catalog_data, migrations.RunPython.noop),
    ]
