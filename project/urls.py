from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Products
    path('api/', include('apps.products.urls')),

    # Account
    path('api/', include('apps.account.urls')),

    # Orders
    path('api/', include('apps.orders.urls')),

    # CMS
    path('api/', include('apps.cms.urls')),

    # Site Config
    path('api/', include('apps.site_config.urls')),

    # Marketing
    path('api/', include('apps.marketing.urls')),

    # cart
    path ('api/', include('apps.cart.urls')),
]

# Add media files serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
