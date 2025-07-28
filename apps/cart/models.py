from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import ProductVariant

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product_variant')

    def __str__(self):
        return f"{self.product_variant} x {self.quantity}"

    def total_price(self):
        return (self.product_variant.price_override or self.product_variant.product.price) * self.quantity
