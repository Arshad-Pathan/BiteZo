from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_category_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="is_cloud_kitchen",
            field=models.BooleanField(default=False),
        ),
    ]
