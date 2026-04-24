"""
Data models for Smart Expense Tracker.
Each Expense belongs to exactly one User — users only ever see their own data.
"""
from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    """Represents a single financial expense recorded by a user."""

    # Predefined categories for clean filtering / display
    CATEGORY_CHOICES = [
        ('Food & Dining',      'Food & Dining'),
        ('Transport',          'Transport'),
        ('Shopping',           'Shopping'),
        ('Entertainment',      'Entertainment'),
        ('Health & Fitness',   'Health & Fitness'),
        ('Bills & Utilities',  'Bills & Utilities'),
        ('Travel',             'Travel'),
        ('Education',          'Education'),
        ('Other',              'Other'),
    ]

    # Link every expense to its owner; deleting a user removes all their expenses
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    title    = models.CharField(max_length=200)
    amount   = models.FloatField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')

    # Date the expense was incurred (user-editable, defaults to today)
    date     = models.DateField()

    # Audit timestamps — not shown to user but useful for admin / debugging
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Most recent expenses appear first in querysets
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} — ₹{self.amount:.2f} ({self.user.username})"