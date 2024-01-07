from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from users.models import CustomUser, Subscription
from django.db.models import Q
from django.core.exceptions import PermissionDenied


class ChessPlayersView(View):
    template_name = 'chess_players/chess_players.html'

    def get(self, request):
        chess_players = CustomUser.objects.filter(Q(role='participant') | Q(role='coach'),
                                                  ~Q(username=request.user.username))
        return render(request, self.template_name, {'chess_players': chess_players})


class ChessPlayerView(View):
    template_name = 'chess_player/chess_player.html'

    def get(self, request, user_id):
        if request.user.user_id == user_id:
            raise PermissionDenied

        chess_player = CustomUser.objects.filter(user_id=user_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        context = {
            'chess_player': chess_player,
            'can_unfollow': Subscription.objects.filter(follower_id=current_user.user_id, target_user_id=chess_player.user_id).first()
        }

        return render(request, self.template_name, context)


class ChessPlayerFollowView(View):
    template_name = 'follow/follow.html'

    def get(self, request, user_id):

        chess_player = get_object_or_404(CustomUser, user_id=user_id)
        return render(request, self.template_name, {'chess_player': chess_player})

    def post(self, request, user_id):
        chess_player = CustomUser.objects.filter(user_id=user_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        Subscription.objects.create(follower_id=current_user.user_id, target_user_id=chess_player.user_id)

        return redirect('chess-players')


class ChessPlayerUnfollowView(View):
    template_name = 'unfollow/unfollow.html'

    def get(self, request, user_id):

        chess_player = get_object_or_404(CustomUser, user_id=user_id)
        return render(request, self.template_name, {'chess_player': chess_player})

    def post(self, request, user_id):
        chess_player = CustomUser.objects.filter(user_id=user_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        subscription = Subscription.objects.filter(follower_id=current_user.user_id, target_user_id=chess_player.user_id)
        subscription.delete()
        return redirect('chess-players')
