from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, CustomerAddress


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    model = Customer
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_guest', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_guest', 'is_staff')
    ordering = ('-date_joined',)
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )


@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'city', 'country', 'is_default')
    search_fields = ('full_name', 'phone', 'city', 'zip_code')
    list_filter = ('country', 'is_default')
    ordering = ('-created_at',)
