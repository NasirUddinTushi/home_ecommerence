from datetime import timedelta
from django.db.models import Count, Sum, F
from django.utils.timezone import now
from django.shortcuts import render
from django.contrib.auth import get_user_model
from unfold.sites import UnfoldAdminSite

from apps.products.models import Product
from apps.orders.models import Order, OrderItem

User = get_user_model()

class DashboardAdminSite(UnfoldAdminSite):
    site_header = "Admin Dashboard"
    site_title  = "Admin"
    index_title = "Overview"
    index_template = "unfold/index.html"

    def index(self, request, extra_context=None):
        today = now().date()

        # ---- Users
        users_total  = User.objects.count()
        users_active = User.objects.filter(is_active=True).count()
        users_guests = User.objects.filter(is_guest=True).count() if hasattr(User, "is_guest") else 0
        users_real   = users_total - users_guests
        users_last7  = User.objects.filter(date_joined__date__gte=today - timedelta(days=6)).count()

        # ---- Orders / Sales
        q_all = Order.objects.select_related("customer").all()

        status_counts = q_all.values("status").annotate(c=Count("id"))
        by_status = {r["status"]: r["c"] for r in status_counts}

        sales_total  = q_all.aggregate(s=Sum("total_amount"))["s"] or 0
        orders_total = q_all.count()
        aov = (sales_total / orders_total) if orders_total else 0

        last7_start = today - timedelta(days=6)
        q_7 = q_all.filter(created_at__date__gte=last7_start)
        sales_7d = q_7.aggregate(s=Sum("total_amount"))["s"] or 0

        # recent orders (latest 10)
        recent_orders = list(q_all.order_by("-created_at")[:10])

        # 7‑day trend (orders per day)
        counts_by_day = q_7.values("created_at__date").annotate(c=Count("id"))
        m = {str(r["created_at__date"]): r["c"] for r in counts_by_day}
        trend, max_count = [], 0
        for i in range(7):
            d = last7_start + timedelta(days=i)
            cnt = int(m.get(str(d), 0))
            trend.append({"date": d, "count": cnt})
            if cnt > max_count: max_count = cnt

        # # cancelled last 30 days
        # cancel_30d = q_all.filter(status="cancelled",
        #                           created_at__date__gte=today - timedelta(days=30)).count()

        # top categories / products by revenue
        top_categories = (
            OrderItem.objects
            .values(name=F("product_variant__product__category__name"))
            .annotate(qty=Sum("quantity"),
                      revenue=Sum(F("quantity") * F("unit_price")))
            .order_by("-revenue")[:5]
        )
        top_products = (
            OrderItem.objects
            .values(name=F("product_variant__product__name"))
            .annotate(qty=Sum("quantity"),
                      revenue=Sum(F("quantity") * F("unit_price")))
            .order_by("-revenue")[:5]
        )

        context = {
            **self.each_context(request),
            "title": "Dashboard",
            "today": today,
            "stats": {
                "users_total": users_total,
                "users_active": users_active,
                "users_guests": users_guests,
                "users_real": users_real,
                "users_last7": users_last7,
                "products": Product.objects.count(),
                "orders": orders_total,
                "pending": by_status.get("pending", 0),
                "processing": by_status.get("processing", 0),
                "shipped": by_status.get("shipped", 0),
                "delivered": by_status.get("delivered", 0),
                "cancelled": by_status.get("cancelled", 0),
                "sales_total": sales_total,
                "sales_7d": sales_7d,
                "aov": aov,
                # "cancel_30d": cancel_30d,
            },
            "recent_orders": recent_orders,
            "trend": trend,
            "trend_max": max_count or 1,
            "top_categories": list(top_categories),
            "top_products": list(top_products),
        }
        return render(request, self.index_template, context)




# --- Create our site instance with the 'admin' namespace ---
admin_site = DashboardAdminSite(name="admin")


# --- Clone default admin registry into our custom site (so all admin:... URLs resolve) ---
from django.contrib import admin as django_admin
from django.contrib.admin.sites import AlreadyRegistered

# Ensure app admin modules are imported
django_admin.autodiscover()

# Copy all registered ModelAdmins from default site to our site
for model, model_admin in django_admin.site._registry.items():
    try:
        admin_site.register(model, model_admin.__class__)
    except AlreadyRegistered:
        pass
