from django import forms
from django.core.exceptions import ValidationError
from .models import Location


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        fields = ['name', 'city', 'address']
        labels = {
            'name': 'Name of location',
            'location': 'City',
            'organizer': 'Address',
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        city = cleaned_data.get('city')
        address = cleaned_data.get('address')

        if name is None and city is None and address is None:
            raise ValidationError('All fields are required.')

        if Location.objects.filter(name=name, city=city, address=address).exists():
            raise ValidationError('This location already exists.')

        return cleaned_data
