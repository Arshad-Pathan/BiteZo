from django.db import migrations, models
import django.db.models.deletion


def copy_current_prices(apps, schema_editor):
    OrderItem = apps.get_model("orders", "OrderItem")
    for item in OrderItem.objects.select_related("product").iterator():
        item.unit_price = item.product.price
        item.save(update_fields=["unit_price"])


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_order_delivery_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivery_address_snapshot",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="unit_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.RunPython(copy_current_prices, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="orderitem",
            name="product",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="products.product"),
        ),
    ]
