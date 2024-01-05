from django.urls import path
from .views import TournamentCommentsView, ReplyCommentView

urlpatterns = [
    path('tournaments/tournament_comments/<int:tournament_id>/', TournamentCommentsView.as_view(), name='tournament_comments'),
    path('tournaments/reply_comment/<int:tournament_id>/<int:comment_id>/', ReplyCommentView.as_view(), name='reply_comment'),
]
