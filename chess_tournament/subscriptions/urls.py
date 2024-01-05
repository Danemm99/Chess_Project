from django.urls import path
from .views import ChessPlayersView, ChessPlayerView, ChessPlayerFollowView, ChessPlayerUnfollowView

urlpatterns = [
    path('chess_players/', ChessPlayersView.as_view(), name='chess-players'),
    path('chess_players/<int:user_id>/', ChessPlayerView.as_view(), name='chess-player'),
    path('chess_players/follow/<int:user_id>/', ChessPlayerFollowView.as_view(), name='follow'),
    path('chess_players/unfollow/<int:user_id>/', ChessPlayerUnfollowView.as_view(), name='unfollow'),
]
