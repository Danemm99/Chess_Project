from django.urls import path
from tournaments.views import TournamentFormView
from .views import (TournamentView, TournamentsView, TournamentEditView, TournamentDeleteView, TournamentRegisterView,
                    TournamentParticipantsView)

urlpatterns = [
    path('home/tournament_creation/', TournamentFormView.as_view(), name='tournament-creation'),
    path('home/tournaments/', TournamentsView.as_view(), name='tournaments'),
    path('home/tournaments/<int:tournament_id>/', TournamentView.as_view(), name='tournament'),
    path('home/tournaments/participants/<int:tournament_id>/', TournamentParticipantsView.as_view(), name='participants-tournament'),
    path('home/tournaments/register/<int:tournament_id>/', TournamentRegisterView.as_view(), name='register-tournament'),
    path('home/tournaments/edit/<int:tournament_id>/', TournamentEditView.as_view(), name='edit-tournament'),
    path('home/tournaments/delete/<int:tournament_id>/', TournamentDeleteView.as_view(), name='delete-tournament'),
]
