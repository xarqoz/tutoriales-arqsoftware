"""URL configuration for Tienda project (Tutorial 01)."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tienda_app.urls')),
]
