from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "homeindurities.com Admin",
    "SITE_HEADER": "homeindurities.com",
    "SITE_SUBHEADER": "Powering your online storefront",

    "SHOW_BACK_BUTTON": True,

    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,
        "navigation": [
            {
                    "title": _("Overview"),
                    "collapsible": False,
                    "items": [
                        {
                            "title": _("Dashboard"),
                            "icon": "dashboard",
                            "link": reverse_lazy("admin:index"), 
                        },
                    ],
                },
            {
                "title": _("Accounts"),
                "collapsible": False,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:account_customer_changelist"),
                    },
                    {
                        "title": _("Password Reset Codes"),
                        "icon": "key",
                        "link": reverse_lazy("admin:account_passwordresetcode_changelist"),
                    },
                    {
                        "title": _("Customer Addresses"),
                        "icon": "location_on",
                        "link": reverse_lazy("admin:account_customeraddress_changelist"),
                    },
                ],
            },
            {
                "title": _("Cart"),
                "collapsible": False,
                "items": [
                    {
                        "title": _("Carts"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:cart_cart_changelist"),
                    },
                    {
                        "title": _("Cart Items"),
                        "icon": "add_shopping_cart",
                        "link": reverse_lazy("admin:cart_cartitem_changelist"),
                    },
                ],
            },
            {
                "title": _("CMS"),
                "collapsible": False,
                "items": [
                    {
                        "title": _("Testimonials"),
                        "icon": "star",
                        "link": reverse_lazy("admin:cms_testimonial_changelist"),
                    },
                    {
                        "title": _("Blog Authors"),
                        "icon": "person",
                        "link": reverse_lazy("admin:cms_blogauthor_changelist"),
                    },
                    {
                        "title": _("Blog Posts"),
                        "icon": "article",
                        "link": reverse_lazy("admin:cms_blogpost_changelist"),
                    },
                    {
                        "title": _("Info Pages"),
                        "icon": "description",
                        "link": reverse_lazy("admin:cms_infopage_changelist"),
                    },
                    {
                        "title": _("Home Sections"),
                        "icon": "view_quilt",
                        "link": reverse_lazy("admin:cms_homesection_changelist"),
                    },

                    {
                        "title": _("Contacts Us"),
                        "icon": "view_quilt",
                        "link": reverse_lazy("admin:cms_contactmessage_changelist"),
                    },
                ],
            },
            {
                "title": _("Marketing"),
                "collapsible": False,
                "items": [
                    {
                        "title": _("Coupons"),
                        "icon": "redeem",
                        "link": reverse_lazy("admin:marketing_coupon_changelist"),
                    },
                    {
                        "title": _("Coupon Usage"),
                        "icon": "history",
                        "link": reverse_lazy("admin:marketing_couponusage_changelist"),
                    },
                    {
                        "title": _("Newsletter Subscribers"),
                        "icon": "email",
                        "link": reverse_lazy("admin:marketing_newslettersubscriber_changelist"),
                    },
                    {
                        "title": _("Featured Products"),
                        "icon": "star",
                        "link": reverse_lazy("admin:marketing_featuredproduct_changelist"),
                    },
                ],
            },
            {
                "title": _("Orders"),
                "collapsible": False,
                "items": [
                    {
                        "title": _("Orders"),
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:orders_order_changelist"),
                    },
                    {
                        "title": _("Order Items"),
                        "icon": "list",
                        "link": reverse_lazy("admin:orders_orderitem_changelist"),
                    },
                ],
            },
            {
                "title": _("Products"),
                "collapsible": False,
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "shopping_bag",
                        "link": reverse_lazy("admin:products_product_changelist"),
                    },
                    {
                        "title": _("Categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:products_category_changelist"),
                    },
                    {
                        "title": _("Attributes"),
                        "icon": "tune",
                        "link": reverse_lazy("admin:products_attribute_changelist"),
                    },
                    {
                        "title": _("Attribute Values"),
                        "icon": "tune",
                        "link": reverse_lazy("admin:products_attributevalue_changelist"),
                    },
                    {
                        "title": _("Variant Values"),
                        "icon": "tune",
                        "link": reverse_lazy("admin:products_productvariantvalue_changelist"),
                    },
                ],
            },
            {
                "title": _("Site Settings"),
                "collapsible": False,
                "items": [
                    {
                        "title": _("Site Configuration"),
                        "icon": "settings",
                        "link": reverse_lazy("admin:site_config_siteconfiguration_changelist"),
                    },
                    {
                        "title": _("Social Links"),
                        "icon": "share",
                        "link": reverse_lazy("admin:site_config_sociallink_changelist"),
                    },
                ],
            },
        ],
    },
}
