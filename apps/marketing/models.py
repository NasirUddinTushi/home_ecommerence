from django.db import models
from apps.products.models import Product

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=[('flat', 'Flat'), ('percent', 'Percentage')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Total number of times the coupon can be used")
    per_user_limit = models.PositiveIntegerField(null=True, blank=True, help_text="Max times a single user can use this")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) 
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('coupon', 'user')

    def __str__(self):
        return f"{self.user.email if self.user else 'Guest'} used {self.coupon.code}"



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
