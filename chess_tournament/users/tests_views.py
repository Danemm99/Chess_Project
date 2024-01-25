from django.test import Client, TestCase
from django.urls import reverse
from users.forms import RegistrationForm
from users.models import CustomUser, Subscription
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_register_view_post_valid_data(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'phone_number': '123456789',
            'email': 'johndoe@example.com',
            'password': 'securepassword',
            'role': 'participant',
        }

        response = self.client.post(self.register_url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user.html')
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].username, 'johndoe')


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')

        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'phone_number': '123456789',
            'email': 'johndoe@example.com',
            'password': make_password('securepassword'),
            'role': 'participant',
        }
        self.user = CustomUser.objects.create(**self.user_data)

    def test_login_view_get_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_login_view_post_valid_credentials(self):
        data = {
            'email': 'johndoe@example.com',
            'password': 'securepassword',
        }

        response = self.client.post(self.login_url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/user.html')
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].username, 'johndoe')


class ChessPlayersViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.chess_players_url = reverse('chess-players')

        self.coach_data = {
            'first_name': 'Coach',
            'last_name': 'User',
            'username': 'coachuser',
            'phone_number': '123456789',
            'email': 'coachuser@example.com',
            'password': make_password('securepassword'),
            'role': 'coach',
        }
        self.coach_user = CustomUser.objects.create(**self.coach_data)

        self.participant_data = {
            'first_name': 'Participant',
            'last_name': 'User',
            'username': 'participantuser',
            'phone_number': '123456789',
            'email': 'participantuser@example.com',
            'password': make_password('securepassword'),
            'role': 'participant',
        }
        self.participant_user = CustomUser.objects.create(**self.participant_data)

    def test_chess_players_view_authenticated_user(self):
        self.client.force_login(self.coach_user)
        response = self.client.get(self.chess_players_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chess_players/chess_players.html')

        self.client.force_login(self.participant_user)
        response = self.client.get(self.chess_players_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chess_players/chess_players.html')


class ChessPlayerViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.coach_data = {
            'first_name': 'Coach',
            'last_name': 'User',
            'username': 'coachuser',
            'phone_number': '123456789',
            'email': 'coachuser@example.com',
            'password': make_password('securepassword'),
            'role': 'coach',
        }
        self.coach_user = CustomUser.objects.create(**self.coach_data)

        self.participant_data = {
            'first_name': 'Participant',
            'last_name': 'User',
            'username': 'participantuser',
            'phone_number': '123456789',
            'email': 'participantuser@example.com',
            'password': make_password('securepassword'),
            'role': 'participant',
        }
        self.participant_user = CustomUser.objects.create(**self.participant_data)

        self.superuser_data = {
            'first_name': 'Super',
            'last_name': 'User',
            'username': 'superuser',
            'phone_number': '123456789',
            'email': 'superuser@example.com',
            'password': make_password('securepassword'),
            'role': 'superuser',
        }
        self.superuser = CustomUser.objects.create(**self.superuser_data)

        self.subscription = Subscription.objects.create(follower=self.coach_user, target_user=self.participant_user)

        self.valid_player_url = reverse('chess-player', args=[self.participant_user.user_id])
        self.self_url = reverse('chess-player', args=[self.coach_user.user_id])
        self.superuser_url = reverse('chess-player', args=[self.superuser.user_id])

    def test_chess_player_view_valid_user(self):
        self.client.force_login(self.coach_user)
        response = self.client.get(self.valid_player_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chess_player/chess_player.html')


class ChessPlayerFollowViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            role='participant'
        )

        self.chess_player = get_user_model().objects.create_user(
            username='chessplayer',
            email='chessplayer@example.com',
            password='chessplayerpassword',
            role='participant'
        )

        self.url = reverse('follow', args=[self.chess_player.user_id])

    def test_get_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_post_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Subscription.objects.filter(
            follower_id=self.user.user_id,
            target_user_id=self.chess_player.user_id
        ).exists())


class ChessPlayerUnfollowViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            role='participant'
        )

        self.chess_player = get_user_model().objects.create_user(
            username='chessplayer',
            email='chessplayer@example.com',
            password='chessplayerpassword',
            role='participant'
        )

        Subscription.objects.create(follower_id=self.user.user_id, target_user_id=self.chess_player.user_id)

        self.url = reverse('unfollow', args=[self.chess_player.user_id])

    def test_get_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_post_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Subscription.objects.filter(
            follower_id=self.user.user_id,
            target_user_id=self.chess_player.user_id
        ).exists())
