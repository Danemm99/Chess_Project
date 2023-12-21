from django.shortcuts import render, redirect
from django.views import View
from .forms import LocationForm
from .models import Location
from users.models import CustomUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


content_type = ContentType.objects.get_for_model(Location)
permission, created = Permission.objects.get_or_create(
    codename='add_location',
    name='Can add location',
    content_type=content_type,
)

coach_users = CustomUser.objects.filter(role='coach')
permission.user_set.set(coach_users)


class LocationAddingView(View):
    template_name = 'location_form/location_form.html'

    def get(self, request):
        form = LocationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LocationForm(request.POST)
        if form.is_valid():
            if request.user.has_perm('locations.add_location'):
                form.save()
                return redirect('home')
            else:
                error_message = "You are not allowed to add locations."
                return render(request, self.template_name, {'form': form, 'error': error_message})

        return render(request, self.template_name, {'form': form})

