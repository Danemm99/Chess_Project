from django.contrib import admin
from .models import CustomUser, Subscription
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import re


class CustomerUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'password', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

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


class SubscriptionAdminForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        follower = cleaned_data.get('follower')
        target_user = cleaned_data.get('target_user')

        if follower and target_user and follower == target_user:
            raise forms.ValidationError("Follower and Target User must be different.")

        return cleaned_data


class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ['profile_image', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'password', 'role']
    fields = ['profile_image', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'password', 'role']
    list_display_links = ['profile_image', 'first_name', 'last_name', 'username', 'phone_number', 'email', 'password', 'role']
    form = CustomerUserAdminForm


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['follower', 'target_user']
    fields = ['follower', 'target_user']
    list_display_links = ['follower', 'target_user']
    form = SubscriptionAdminForm


admin.site.register(CustomUser, CustomerUserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
