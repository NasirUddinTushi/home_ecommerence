from django.contrib.admin.apps import AdminConfig

class MyAdminConfig(AdminConfig):
    default_site = "project.admin_site.DashboardAdminSite"
