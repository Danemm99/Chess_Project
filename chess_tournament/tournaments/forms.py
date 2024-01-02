from django import forms
from django.core.exceptions import ValidationError
from .models import Tournament
from locations.models import Location


class BaseTournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        fields = ['name', 'location', 'prizes', 'date', 'registration_deadline']
        labels = {
            'name': 'Name of the tournament',
            'location': 'Location',
            'prizes': 'Prizes',
            'date': 'Date',
            'registration_deadline': 'Deadline of registration'
        }
        widgets = {
            'organizer': forms.HiddenInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     default_location = Location.objects.get_or_create(name=None)
    #     self.fields['location'].initial = default_location

    def clean_date(self):
        date_value = self.cleaned_data.get('date')
        registration_deadline_value = self.cleaned_data.get('registration_deadline')

        if date_value and registration_deadline_value and date_value <= registration_deadline_value:
            raise ValidationError('The tournament date must be later than the registration deadline.')

        return date_value


class TournamentForm(BaseTournamentForm):

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if name and Tournament.objects.filter(name=name).exists():
            raise ValidationError('The tournament with this name already exists.')

        return name


class TournamentEditForm(BaseTournamentForm):
    pass
