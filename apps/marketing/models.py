from django.db import models
from apps.products.models import Product



class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="featured_entries")
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Featured: {self.product.name}"
