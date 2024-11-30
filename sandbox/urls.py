"""
URL configuration.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('api.urls')),
    path('', include('gateway.urls')),
    path('admin/', admin.site.urls),
]
