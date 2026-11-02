from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_cloudkitchen_proxy"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="chef_name",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="chef_image",
            field=models.ImageField(blank=True, null=True, upload_to="chefs/"),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="chef_bio",
            field=models.TextField(blank=True),
        ),
    ]
