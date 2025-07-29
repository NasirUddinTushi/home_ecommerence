from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin 
from .models import Customer, CustomerAddress, PasswordResetCode


@admin.register(Customer)
class CustomerAdmin(BaseUserAdmin, ModelAdmin):  # Combine both
    model = Customer
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )


@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(ModelAdmin):
    list_display = ('email', 'code', 'is_used', 'created_at', 'reset_token')
    search_fields = ('email', 'code', 'reset_token')
    list_filter = ('is_used', 'created_at')
    ordering = ('-created_at',)


@admin.register(CustomerAddress)
class CustomerAddressAdmin(ModelAdmin):
    list_display = ('get_full_name', 'phone', 'city', 'country', 'is_default')
    search_fields = ('first_name', 'last_name', 'phone', 'city', 'postal_code')
    list_filter = ('country', 'is_default')
    ordering = ('-created_at',)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    get_full_name.short_description = 'Full Name'
