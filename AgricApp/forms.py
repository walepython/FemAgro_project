from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage
import re


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 000-0000'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'How can we help?'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us more about your needs...',
                'rows': 5
            }),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'your@email.com'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

# ── Disposable email domains to block ─────────────
BLOCKED_DOMAINS = [
    'mailinator.com', 'tempmail.com', 'guerrillamail.com',
    'throwaway.email', 'yopmail.com', '10minutemail.com',
    'trashmail.com', 'fakeinbox.com', 'sharklasers.com',
    'guerrillamailblock.com', 'grr.la', 'guerrillamail.info',
    'spam4.me', 'dispostable.com', 'mailnull.com',
]

class DonationForm(forms.Form):

    donor_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. Emeka Adeyemi',
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
        })
    )

    amount = forms.DecimalField(
        min_value=100,
        max_value=10000000,   # ← cap at ₦10 million
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'e.g. 5000',
            'min': '100',
        })
    )

    anonymous = forms.BooleanField(required=False)
    monthly   = forms.BooleanField(required=False)

    # ── Email validation ────────────────────────
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()

        # Basic format check
        if not re.match(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError(
                'Please enter a valid email address.'
            )

        # Block disposable emails
        domain = email.split('@')[-1]
        if domain in BLOCKED_DOMAINS:
            raise forms.ValidationError(
                'Temporary or disposable email addresses are not allowed. '
                'Please use your real email.'
            )

        # Block emails with suspicious patterns
        suspicious = ['+test', 'test@', 'fake@', 'noreply@',
                      'spam@', 'trash@', 'delete@']
        if any(p in email for p in suspicious):
            raise forms.ValidationError(
                'Please use a real email address.'
            )

        return email

    # ── Name validation ─────────────────────────
    def clean_donor_name(self):
        name = self.cleaned_data.get('donor_name', '').strip()

        if name:
            # Only letters, spaces, hyphens, apostrophes
            if not re.match(r"^[a-zA-Z\s\-'\.]{2,100}$", name):
                raise forms.ValidationError(
                    'Name can only contain letters, spaces, and hyphens.'
                )

            # Block obvious fake names
            fake_names = ['test', 'asdf', 'qwerty', 'anonymous',
                          '123', 'xxx', 'abc', 'aaaa']
            if name.lower() in fake_names:
                raise forms.ValidationError(
                    'Please enter your real name.'
                )

        return name

    # ── Amount validation ───────────────────────
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        if amount is None:
            raise forms.ValidationError('Please enter a donation amount.')

        if amount < 100:
            raise forms.ValidationError(
                'Minimum donation is ₦100.'
            )

        if amount > 10000000:
            raise forms.ValidationError(
                'Maximum single donation is ₦10,000,000. '
                'Contact us for larger donations.'
            )

        return amount
