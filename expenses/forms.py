"""
Django forms for Smart Expense Tracker.
Forms handle both rendering widgets in templates AND server-side validation.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Expense


class SignupForm(UserCreationForm):
    """
    Extends Django's built-in UserCreationForm to add an email field.
    Passwords are hashed automatically by the parent class.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'you@example.com',
        })
    )

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap classes and placeholders to all inherited fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password',
        })

    def save(self, commit=True):
        """
        Save user with email only.
        Username is the single identity field — no first_name/last_name used.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # first_name and last_name intentionally left blank
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Simple login form — Django's authenticate() handles the actual check.
    We build this manually so we can apply Bootstrap styling easily.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
        'autofocus': True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))


class ExpenseForm(forms.ModelForm):
    """
    ModelForm for creating and editing expenses.
    The 'user' field is excluded — it's set programmatically in the view.
    """

    class Meta:
        model  = Expense
        # Explicitly list fields so 'user' is never exposed to the client
        fields = ['title', 'amount', 'category', 'date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Lunch at restaurant',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',   # Renders native date picker in browsers
            }),
        }

    def clean_amount(self):
        """Ensure amount is positive."""
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount