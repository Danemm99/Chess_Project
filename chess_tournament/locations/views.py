from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render, redirect
from .forms import LocationForm


class LocationAddingView(View):
    template_name = 'location_form/location_form.html'

    @method_decorator(permission_required('locations.add_location', raise_exception=True))
    def get(self, request):
        form = LocationForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(permission_required('locations.add_location', raise_exception=True))
    def post(self, request):
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

        return render(request, self.template_name, {'form': form})


