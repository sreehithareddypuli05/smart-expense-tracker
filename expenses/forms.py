"""
Django forms for Smart Expense Tracker.
Forms handle both rendering widgets in templates AND server-side validation.
"""
import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Expense


class SignupForm(UserCreationForm):
    """
    Signup form with explicit first_name and last_name fields.
    If the user leaves them blank, we attempt to extract from the email.
    """

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Sreehitha',
        })
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Reddypuli',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'you@example.com',
        })
    )

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def _extract_names_from_email(self, email):
        """
        Fallback: parse first/last name from email local part.
        sreehithareddypuli@gmail.com -> ('Sreehithareddypuli', '')
        john.doe@gmail.com           -> ('John', 'Doe')
        jane_smith@yahoo.com         -> ('Jane', 'Smith')
        """
        local = email.split('@')[0]
        parts = [p.capitalize() for p in re.split(r'[._\-]+', local) if p]
        if len(parts) >= 2:
            return parts[0], parts[-1]
        elif len(parts) == 1:
            return parts[0], ''
        return '', ''

    def save(self, commit=True):
        """
        Save the user.
        - If first_name / last_name were typed -> use them directly.
        - If left blank -> extract from email as best-effort fallback.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        first = self.cleaned_data.get('first_name', '').strip()
        last  = self.cleaned_data.get('last_name',  '').strip()

        if first or last:
            user.first_name = first
            user.last_name  = last
        else:
            user.first_name, user.last_name = self._extract_names_from_email(
                self.cleaned_data['email']
            )

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Simple login form."""
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
    """ModelForm for creating and editing expenses."""

    class Meta:
        model  = Expense
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
                'type': 'date',
            }),
        }

    def clean_amount(self):
        """Ensure amount is positive."""
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount