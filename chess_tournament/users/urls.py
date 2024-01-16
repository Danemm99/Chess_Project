from django.urls import path
from .views import (RegisterView, LoginView, LogoutView, HomeView, HomeEditView, MainView,
                    ChessPlayersView, ChessPlayerView, ChessPlayerFollowView, ChessPlayerUnfollowView)

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('home/edit_profile/', HomeEditView.as_view(), name='edit-profile'),
    path('home/chess_players/', ChessPlayersView.as_view(), name='chess-players'),
    path('home/chess_players/<int:user_id>/', ChessPlayerView.as_view(), name='chess-player'),
    path('home/chess_players/<int:user_id>/follow/', ChessPlayerFollowView.as_view(), name='follow'),
    path('home/chess_players/<int:user_id>/unfollow/', ChessPlayerUnfollowView.as_view(), name='unfollow'),
]
