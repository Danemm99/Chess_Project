from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .models import CustomUser
import re


class BaseUserForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('coach', 'Coach'),
        ('participant', 'Participant'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    profile_image = forms.FileField(required=False, label='File')

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


class RegistrationForm(BaseUserForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email


class HomeEditForm(BaseUserForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
