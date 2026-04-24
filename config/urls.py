"""
Root URL configuration for Smart Expense Tracker.
All expense-related URLs are delegated to the expenses app.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin (keep for superuser management)
    path('admin/', admin.site.urls),

    # All app URLs live in expenses/urls.py
    path('', include('expenses.urls')),
]