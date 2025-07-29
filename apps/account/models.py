from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Custom User Model (Customer)
class Customer(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=255, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=255, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    # phone = models.CharField(_("phone number"), max_length=20, blank=True, null=True)
    # avatar = models.ImageField(_("avatar"), upload_to="avatars/", blank=True, null=True)
    is_guest = models.BooleanField(default=False)  # For guest checkout
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name if self.first_name else self.email

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else None

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")
        ordering = ['-date_joined']


# Customer Address Model
class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Bangladesh")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()



class PasswordResetCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    reset_token = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=1)