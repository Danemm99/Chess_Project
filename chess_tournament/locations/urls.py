from django.urls import path
from locations.views import LocationAddingView

urlpatterns = [
    path('home/location_adding/', LocationAddingView.as_view(), name='location-adding'),
]
