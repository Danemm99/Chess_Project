from django.urls import path
from tournaments.views import TournamentFormView
from .views import (TournamentView, TournamentsView, TournamentEditView, TournamentDeleteView, TournamentRegisterView,
                    TournamentParticipantsView, TournamentCommentsView, ReplyCommentView)

urlpatterns = [
    path('tournament_creation/', TournamentFormView.as_view(), name='tournament-creation'),
    path('tournaments/', TournamentsView.as_view(), name='tournaments'),
    path('tournaments/<int:tournament_id>/', TournamentView.as_view(), name='tournament'),
    path('tournaments/participants/<int:tournament_id>/', TournamentParticipantsView.as_view(),
         name='participants-tournament'),
    path('tournaments/register/<int:tournament_id>/', TournamentRegisterView.as_view(), name='register-tournament'),
    path('tournaments/edit/<int:tournament_id>/', TournamentEditView.as_view(), name='edit-tournament'),
    path('tournaments/delete/<int:tournament_id>/', TournamentDeleteView.as_view(), name='delete-tournament'),
    path('tournaments/tournament_comments/<int:tournament_id>/', TournamentCommentsView.as_view(),
         name='tournament_comments'),
    path('tournaments/reply_comment/<int:tournament_id>/<int:comment_id>/', ReplyCommentView.as_view(),
         name='reply_comment'),
]
