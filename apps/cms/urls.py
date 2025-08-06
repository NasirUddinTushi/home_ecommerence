from django.urls import path
from .views import (
    TestimonialListAPIView, BlogListAPIView, BlogDetailAPIView,
    InfoPageDetailAPIView, HomeSectionListAPIView, ContactUsAPIView
)

urlpatterns = [
    path('cms/testimonials/', TestimonialListAPIView.as_view(), name='testimonial-list'),
    path('cms/blogs/', BlogListAPIView.as_view(), name='blog-list'),
    path('cms/blogs/<slug:slug>/', BlogDetailAPIView.as_view(), name='blog-detail'),
    path('cms/pages/<slug:slug>/', InfoPageDetailAPIView.as_view(), name='info-page'),
    path('cms/home-sections/', HomeSectionListAPIView.as_view(), name='home-sections'),
    path('contact/', ContactUsAPIView.as_view(), name='contact-us'),
]
