from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import CustomUser
import re


class RegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('coach', 'Coach'),
        ('participant', 'Participant'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'email', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('A user with that email already exists.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        return make_password(password)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_regex = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_regex.match(phone_number):
            raise ValidationError('Please enter a valid phone number.')

        return phone_number


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
