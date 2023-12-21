import pytest
from django.test import Client
from django.contrib.auth.models import User
from tournaments.models import Tournament


@pytest.mark.django_db
def test_only_coach_can_create_tournament():
    pass

    # coach_user = User.objects.create_user(username='coach',
    #                                       password='password',
    #                                       role='coach',
    #                                       email='nnn@gmail.com',
    #                                       first_name='Bob',
    #                                       last_name='Span',
    #                                       phone_number='+380688656388')
    #
    # participant_user = User.objects.create_user(username='participant',
    #                                             password='password',
    #                                             role='participant',
    #                                             email='mmm@gmail.com',
    #                                             first_name='Bob',
    #                                             last_name='Span',
    #                                             phone_number='+380688656388')
    #
    # client_coach = Client()
    # client_coach.force_login(coach_user)
    #
    # client_participant = Client()
    # client_participant.force_login(participant_user)
    #
    # response_coach = client_coach.post('/home/tournament_creation/', {
    #     'name': 'Test Tournament',
    #     'location': 1,
    #     'prizes': 'Призи',
    #     'date': '2023-12-31',
    #     'registration_deadline': '2023-12-25'
    # })
    #
    # assert response_coach.status_code == 302
    # assert Tournament.objects.filter(name='Test Tournament').exists()
    #
    # response_participant = client_participant.post('/home/tournament_creation/', {
    #     'name': 'Test Tournament 2',
    #     'location': 1,
    #     'prizes': 'Призи',
    #     'date': '2023-12-31',
    #     'registration_deadline': '2023-12-25'
    # })
    #
    # assert response_participant.status_code == 200
    # assert not Tournament.objects.filter(name='Test Tournament 2').exists()





