from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_restaurant_is_cloud_kitchen"),
    ]

    operations = [
        migrations.CreateModel(
            name="CloudKitchen",
            fields=[],
            options={
                "verbose_name": "cloud kitchen",
                "verbose_name_plural": "cloud kitchens",
                "proxy": True,
            },
            bases=("products.restaurant",),
        ),
    ]
