from django.contrib import admin
from .models import Location
from tournaments.models import Tournament
from users.models import CustomUser
from tournaments.admin import TournamentAdminForm


class TournamentInline(admin.TabularInline):
    model = Tournament
    form = TournamentAdminForm
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'organizer':
            kwargs['queryset'] = CustomUser.objects.filter(role='coach')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address']
    fields = ['name', 'city', 'address']
    list_display_links = ['name', 'city', 'address']
    inlines = [TournamentInline]


admin.site.register(Location, LocationAdmin)
