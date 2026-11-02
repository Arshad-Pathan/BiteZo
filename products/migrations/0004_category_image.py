from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_restaurant_pages"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="categories/"),
        ),
    ]
