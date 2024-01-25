from django.urls import path
from tournaments.views import TournamentFormView
from .views import (TournamentView, TournamentsView, TournamentEditView, TournamentDeleteView, TournamentRegisterView,
                    TournamentParticipantsView, TournamentParticipantView, ParticipantFollowView,
                    ParticipantUnfollowView, ReplyCommentView, CommentatorView, CommentFollowView, CommentUnfollowView)

urlpatterns = [
    path('tournament_creation/', TournamentFormView.as_view(), name='tournament-creation'),
    path('tournaments/', TournamentsView.as_view(), name='tournaments'),
    path('tournaments/<int:tournament_id>/', TournamentView.as_view(), name='tournament'),
    path('tournaments/<int:tournament_id>/participants/', TournamentParticipantsView.as_view(),
         name='participants-tournament'),
    path('tournaments/<int:tournament_id>/participants/<int:participant_id>/', TournamentParticipantView.as_view(),
         name='participant-tournament'),
    path('tournaments/<int:tournament_id>/participants/<int:participant_id>/follow/', ParticipantFollowView.as_view(),
         name='follow-tournament'),
    path('tournaments/<int:tournament_id>/participants/<int:participant_id>/unfollow/', ParticipantUnfollowView.as_view(),
         name='unfollow-tournament'),
    path('tournaments/<int:tournament_id>/commentator/<int:commentator_id>/', CommentatorView.as_view(),
         name='commentator-tournament'),
    path('tournaments/<int:tournament_id>/commentator/<int:commentator_id>/follow/', CommentFollowView.as_view(),
         name='commentator-follow-tournament'),
    path('tournaments/<int:tournament_id>/commentator/<int:commentator_id>/unfollow/', CommentUnfollowView.as_view(),
         name='commentator-unfollow-tournament'),
    path('tournaments/<int:tournament_id>/register/', TournamentRegisterView.as_view(), name='register-tournament'),
    path('tournaments/<int:tournament_id>/edit/', TournamentEditView.as_view(), name='edit-tournament'),
    path('tournaments/<int:tournament_id>/delete/', TournamentDeleteView.as_view(), name='delete-tournament'),
    path('tournaments/<int:tournament_id>/reply_comment/<int:comment_id>/', ReplyCommentView.as_view(),
         name='reply-comment'),
]
