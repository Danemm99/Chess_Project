import pytest
from django.test import Client
from users.models import CustomUser


@pytest.mark.django_db
def test_coach_can_create_tournament():

    coach_user = CustomUser.objects.create_user(
        username='coach',
        password='password',
        role='coach',
        email='nnn@gmail.com',
        first_name='Bob',
        last_name='Span',
        phone_number='+380688656388'
    )

    client_coach = Client()
    client_coach.force_login(coach_user)

    response = client_coach.get('/home/tournament_creation/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_participant_cannot_create_tournament():

    participant_user = CustomUser.objects.create_user(
        username='participant',
        password='password',
        role='participant',
        email='mmm@gmail.com',
        first_name='Bob',
        last_name='Span',
        phone_number='+380688656388'
    )

    client_participant = Client()
    client_participant.force_login(participant_user)

    response = client_participant.get('/home/tournament_creation/')

    assert response.status_code == 403
