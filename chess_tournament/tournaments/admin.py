from django import forms
from django.contrib import admin
from .models import Tournament, Participant, Comment
from users.models import CustomUser
from django.core.exceptions import ValidationError


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0
    fields = ['user']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = CustomUser.objects.filter(role='participant')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TournamentAdminForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = '__all__'

    def clean_date(self):
        date = self.cleaned_data.get("date")
        registration_deadline = self.cleaned_data.get("registration_deadline")

        if date and registration_deadline and registration_deadline >= date:
            raise ValidationError('The tournament date must be later than the registration deadline.')

        return date

    def clean(self):
        self.clean_date()


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'prizes', 'date', 'registration_deadline', 'location', 'organizer']
    fields = ['name', 'prizes', 'date', 'registration_deadline', 'location', 'organizer']
    list_display_links = ['name', 'prizes', 'date', 'registration_deadline', 'location', 'organizer']
    inlines = [ParticipantInline]
    form = TournamentAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organizer':
            kwargs['queryset'] = CustomUser.objects.filter(role='coach')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'user']
    fields = ['tournament', 'user']
    list_display_links = ['tournament', 'user']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = CustomUser.objects.filter(role='participant')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'tournament', 'parent_comment']
    fields = ['content', 'user', 'tournament', 'parent_comment']
    list_display_links = ['content', 'user', 'tournament', 'parent_comment']


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Comment, CommentAdmin)
