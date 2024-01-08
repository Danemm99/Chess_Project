from django.views import View
from django.shortcuts import render, redirect
from .forms import LocationForm
from django.core.exceptions import PermissionDenied


class PermissionMixin:
    @staticmethod
    def check_coach_permission(request):
        if not request.user.groups.filter(name='Coaches').exists():
            raise PermissionDenied

    @staticmethod
    def check_participant_permission(request):
        if not request.user.groups.filter(name='Participants').exists():
            raise PermissionDenied


class LocationAddingView(PermissionMixin, View):
    template_name = 'location_form/location_form.html'

    def get(self, request):
        self.check_coach_permission(request)
        form = LocationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        self.check_coach_permission(request)
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

        return render(request, self.template_name, {'form': form})



