"""
URL patterns for the expenses app.
All paths are relative to the project root (config/urls.py includes this).
"""
from django.urls import path
from . import views

urlpatterns = [
    # ── Root redirect ──────────────────────────────────────────────────────
    path('', lambda request: __import__('django.shortcuts', fromlist=['redirect']).redirect('dashboard'), name='home'),

    # ── Auth ───────────────────────────────────────────────────────────────
    path('signup/',    views.signup_view,  name='signup'),
    path('login/',     views.login_view,   name='login'),
    path('logout/',    views.logout_view,  name='logout'),

    # ── Expenses ───────────────────────────────────────────────────────────
    path('dashboard/',          views.dashboard,     name='dashboard'),
    path('expenses/add/',       views.add_expense,   name='add_expense'),
    path('expenses/<int:pk>/edit/',   views.edit_expense,  name='edit_expense'),
    path('expenses/<int:pk>/delete/', views.delete_expense, name='delete_expense'),
]