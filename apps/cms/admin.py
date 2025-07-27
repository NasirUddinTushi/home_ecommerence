from django.contrib import admin
from .models import Testimonial, BlogPost, BlogAuthor, InfoPage, HomeSection


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'rating', 'created_at')
    search_fields = ('customer_name', 'message')
    ordering = ('-created_at',)


@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title',)


@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order',)
