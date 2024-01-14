from django.urls import path
from tournaments.views import TournamentFormView
from .views import (TournamentView, TournamentsView, TournamentEditView, TournamentDeleteView, TournamentRegisterView,
                    TournamentParticipantsView, TournamentCommentsView, ReplyCommentView)

urlpatterns = [
    path('tournament_creation/', TournamentFormView.as_view(), name='tournament-creation'),
    path('tournaments/', TournamentsView.as_view(), name='tournaments'),
    path('tournaments/<int:tournament_id>/', TournamentView.as_view(), name='tournament'),
    path('tournaments/<int:tournament_id>/participants/', TournamentParticipantsView.as_view(),
         name='participants-tournament'),
    path('tournaments/<int:tournament_id>/register/', TournamentRegisterView.as_view(), name='register-tournament'),
    path('tournaments/<int:tournament_id>/edit/', TournamentEditView.as_view(), name='edit-tournament'),
    path('tournaments/<int:tournament_id>/delete/', TournamentDeleteView.as_view(), name='delete-tournament'),
    path('tournaments/<int:tournament_id>/tournament_comments/', TournamentCommentsView.as_view(),
         name='tournament-comments'),
    path('tournaments/<int:tournament_id>/reply_comment/<int:comment_id>/', ReplyCommentView.as_view(),
         name='reply-comment'),
]
