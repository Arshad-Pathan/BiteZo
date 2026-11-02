from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0007_chef_profile"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="restaurant",
            name="chef_bio",
        ),
        migrations.RemoveField(
            model_name="restaurant",
            name="chef_image",
        ),
        migrations.RemoveField(
            model_name="restaurant",
            name="chef_name",
        ),
    ]
