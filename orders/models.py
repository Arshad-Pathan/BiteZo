from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    delivery_address = models.ForeignKey(
        "customers.DeliveryAddress",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    delivery_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    delivery_address_snapshot = models.TextField(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    payment_successful = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"Order #{self.id}"

    @property
    def items_total(self):
        total = 0
        for item in self.items.all():
            total += item.subtotal
        return total

    @property
    def total_price(self):
        return self.items_total + self.delivery_fee

    @property
    def delivery_status(self):
        elapsed_seconds = (
            timezone.now() - self.created_at
        ).total_seconds()

        elapsed_minutes = elapsed_seconds / 60
        if elapsed_minutes < 5:
            return "Order Placed"
        elif elapsed_minutes < 10:
            return "Confirmed"
        elif elapsed_minutes < 15:
            return "Preparing"
        elif elapsed_minutes < 20:
            return "Picked Up"
        elif elapsed_minutes < 30:
            return "Out for Delivery"
        else:
            return "Delivered"


    # @property
    # def delivery_status(self):
    #     elapsed_seconds = (
    #         timezone.now() - self.created_at
    #     ).total_seconds()

    #     elapsed_minutes = elapsed_seconds

    #     if elapsed_minutes < 5:
    #         return "Order Placed"
    #     elif elapsed_minutes < 10:
    #         return "Confirmed"
    #     elif elapsed_minutes < 15:
    #         return "Preparing"
    #     elif elapsed_minutes < 20:
    #         return "Picked Up"
    #     elif elapsed_minutes < 30:
    #         return "Out for Delivery"
    #     else:
    #         return "Delivered"



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
