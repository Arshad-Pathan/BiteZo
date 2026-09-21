from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    payment_successful = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"Order #{self.id}"

    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total

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
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
