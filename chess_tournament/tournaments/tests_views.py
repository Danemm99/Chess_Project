from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from tournaments.models import Tournament, Comment, Participant
from tournaments.forms import TournamentEditForm
from locations.models import Location


class TournamentsViewTest(TestCase):
    def setUp(self):
        self.organizer = get_user_model().objects.create_user(
            username='organizer',
            email='organizer@example.com',
            password='organizerpassword',
            role='coach'
        )

        self.location = Location.objects.create(name='Test Location', city='New York', address='Alibaba')

        self.tournament = Tournament.objects.create(
            location=self.location,
            name='Test Tournament',
            organizer=self.organizer,
            prizes='Prizes for the tournament',
            date='2024-11-01',
            registration_deadline='2024-01-01',
        )

        self.url = reverse('tournaments')

        self.client = Client()

    def test_tournaments_view(self):
        self.client.login(username='organizer', password='organizerpassword')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Tournament')


class TournamentViewTest(TestCase):
    def setUp(self):
        self.organizer = get_user_model().objects.create_user(
            username='organizer',
            email='organizer@example.com',
            password='organizerpassword',
            role='coach'
        )

        self.location = Location.objects.create(name='Test Location', city='New York', address='Alibaba')

        self.tournament = Tournament.objects.create(
            location=self.location,
            name='Test Tournament',
            organizer=self.organizer,
            prizes='Prizes for the tournament',
            date='2024-11-01',
            registration_deadline='2024-01-01',
        )

        self.url = reverse('tournament', args=[self.tournament.tournament_id])

        self.client = Client()

    def test_tournament_view(self):
        self.client.login(username='organizer', password='organizerpassword')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_tournament_view_post_comment(self):
        self.client.login(username='organizer', password='organizerpassword')

        response = self.client.post(self.url, {'content': 'Test Comment'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)

        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'Test Comment')


class TournamentEditViewTest(TestCase):
    def setUp(self):
        self.organizer = get_user_model().objects.create_user(
            username='organizer',
            email='organizer@example.com',
            password='organizerpassword',
            role='coach'
        )

        self.location = Location.objects.create(name='Test Location', city='New York', address='Alibaba')

        self.tournament = Tournament.objects.create(
            location=self.location,
            name='Test Tournament',
            organizer=self.organizer,
            prizes='Prizes for the tournament',
            date='2024-01-01',
            registration_deadline='2024-12-31',
        )

        self.url = reverse('edit-tournament', args=[self.tournament.tournament_id])

        self.client = Client()

    def test_tournament_edit_view_get(self):
        self.client.login(username='organizer', password='organizerpassword')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit tournament')
        self.assertIsInstance(response.context['form'], TournamentEditForm)
        self.assertEqual(response.context['tournament'], self.tournament)

    def test_tournament_edit_view_post_valid(self):
        self.client.login(username='organizer', password='organizerpassword')

        response = self.client.post(self.url, {
            'location': self.location.location_id,
            'name': 'Updated Test Tournament',
            'organizer': self.organizer,
            'prizes': 'Prizes for the tournament',
            'date': '2024-12-30',
            'registration_deadline': '2024-12-29',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tournament', args=[self.tournament.tournament_id]))

        self.tournament.refresh_from_db()

        self.assertEqual(self.tournament.name, 'Updated Test Tournament')
        self.assertEqual(str(self.tournament.date), '2024-12-30')
        self.assertEqual(str(self.tournament.registration_deadline), '2024-12-29')


class TournamentRegisterViewTest(TestCase):
    def setUp(self):
        self.organizer = get_user_model().objects.create_user(
            username='organizer',
            email='organizer@example.com',
            password='organizerpassword',
            role='coach'
        )

        self.location = Location.objects.create(name='Test Location', city='New York', address='Alibaba')

        self.tournament = Tournament.objects.create(
            location=self.location,
            name='Test Tournament',
            organizer=self.organizer,
            prizes='Prizes for the tournament',
            date='2024-01-01',
            registration_deadline='2024-12-31',
        )

        self.url = reverse('register-tournament', args=[self.tournament.tournament_id])

        self.client = Client()

        self.participant = get_user_model().objects.create_user(
            username='participant',
            email='participant@example.com',
            password='participantpassword',
            role='participant'
        )

    def test_tournament_register_view_get(self):
        self.client.login(username='participant', password='participantpassword')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_tournament/register_tournament.html')
        self.assertEqual(response.context['tournament'], self.tournament)

    def test_tournament_register_view_post(self):
        self.client.login(username='participant', password='participantpassword')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tournament', args=[self.tournament.tournament_id]))

        self.assertTrue(Participant.objects.filter(tournament_id=self.tournament.tournament_id,
                                                   user_id=self.participant.user_id).exists())
