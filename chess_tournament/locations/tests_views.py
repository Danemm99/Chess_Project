from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from locations.models import Location
from .forms import LocationForm


class LocationAddingViewTest(TestCase):
    def setUp(self):
        self.coach = get_user_model().objects.create_user(
            username='coach',
            email='coach@example.com',
            password='coachpassword',
            role='coach'
        )

        self.url = reverse('location-adding')

        self.client = Client()

    def test_location_adding_view_get(self):
        self.client.login(username='coach', password='coachpassword')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'location_form/location_form.html')
        self.assertIsInstance(response.context['form'], LocationForm)

    def test_location_adding_view_post_valid(self):
        self.client.login(username='coach', password='coachpassword')

        response = self.client.post(self.url, {'name': 'Test Location', 'city': 'Test City', 'address': 'Test Address'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        self.assertTrue(Location.objects.filter(name='Test Location', city='Test City', address='Test Address').exists())
