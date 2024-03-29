from .forms import RegistrationForm, LoginForm, HomeEditForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from users.models import CustomUser, Subscription
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from tournaments.views import SubscriptionMixin


class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            user = CustomUser.get_by_email(email)
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'login/login.html'

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.get_by_email(email)

            if user and check_password(password, user.password) and (user.role == 'participant' or
                                                                     user.role == 'coach'):
                login(request, user)
                return redirect('home')
            else:
                return render(request, self.template_name, {'form': form, 'error': 'Invalid email or password.'})
        return render(request, self.template_name, {'form': form, 'error': 'Invalid email or password.'})


class LogoutView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('main')


class HomeView(View):
    template_name_participant = 'participant/participant.html'
    template_name_coach = 'coach/coach.html'
    template_name = 'user/user.html'

    def get(self, request):
        if not request.user.is_coach and not request.user.is_participant:
            raise PermissionDenied

        user = request.user
        context = {'user': user, 'permission_create_tournament': user.groups.filter(name='Coaches').exists(),
                   'permission_add_location': user.groups.filter(name='Coaches').exists()}

        return render(request, self.template_name, context)


class HomeEditView(View):
    template_name = 'user_edit/user_edit.html'

    def get(self, request):
        user = get_object_or_404(CustomUser, user_id=request.user.user_id)
        form = HomeEditForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user = get_object_or_404(CustomUser, user_id=request.user.user_id)
        form = HomeEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class MainView(View):
    template_name = 'main/main.html'

    def get(self, request):
        return render(request, self.template_name)


class ChessPlayersView(View):
    template_name = 'chess_players/chess_players.html'

    def get(self, request):
        chess_players = CustomUser.objects.filter(Q(role='participant') | Q(role='coach'),
                                                  ~Q(username=request.user.username))
        res = []

        for chess_player in chess_players:
            res.append(tuple([chess_player,
                              Subscription.objects.filter(target_user_id=chess_player.user_id).count(),
                              Subscription.objects.filter(follower_id=chess_player.user_id).count()]))

        return render(request, self.template_name, {
            'res': res,
        })


class ChessPlayerView(View):
    template_name = 'chess_player/chess_player.html'

    def get(self, request, user_id):
        if request.user.user_id == user_id or CustomUser.objects.filter(user_id=user_id).first().role == 'superuser':
            raise PermissionDenied

        chess_player = CustomUser.objects.filter(user_id=user_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        context = {
            'chess_player': chess_player,
            'can_unfollow': Subscription.objects.filter(follower_id=current_user.user_id,
                                                        target_user_id=chess_player.user_id).first()
        }

        return render(request, self.template_name, context)


class ChessPlayerFollowView(View, SubscriptionMixin):
    template_name = 'follow/follow.html'

    def get(self, request, user_id):
        if request.user.user_id == user_id or CustomUser.objects.filter(user_id=user_id).first().role == 'superuser':
            raise PermissionDenied

        if self.check_subscription(request, user_id):
            raise PermissionDenied

        chess_player = get_object_or_404(CustomUser, user_id=user_id)

        return render(request, self.template_name, {'chess_player': chess_player})

    def post(self, request, user_id):
        chess_player = CustomUser.objects.filter(user_id=user_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        Subscription.objects.create(follower_id=current_user.user_id, target_user_id=chess_player.user_id)

        return redirect('chess-player', user_id)


class ChessPlayerUnfollowView(View, SubscriptionMixin):
    template_name = 'unfollow/unfollow.html'

    def get(self, request, user_id):
        if request.user.user_id == user_id or CustomUser.objects.filter(user_id=user_id).first().role == 'superuser':
            raise PermissionDenied

        if not self.check_subscription(request, user_id):
            raise PermissionDenied

        chess_player = get_object_or_404(CustomUser, user_id=user_id)

        return render(request, self.template_name, {'chess_player': chess_player})

    def post(self, request, user_id):
        chess_player = CustomUser.objects.filter(user_id=user_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        subscription = Subscription.objects.filter(follower_id=current_user.user_id, target_user_id=chess_player.user_id)
        subscription.delete()

        return redirect('chess-player', user_id)
