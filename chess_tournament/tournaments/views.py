from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TournamentForm, TournamentEditForm
from .models import Tournament, Participant
from locations.models import Location
from users.models import CustomUser
from datetime import datetime
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied


class TournamentFormView(View):
    template_name = 'tournament_form/tournament_form.html'

    @method_decorator(permission_required('tournaments.create_tournament', raise_exception=True))
    def get(self, request):
        form = TournamentForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(permission_required('tournaments.create_tournament', raise_exception=True))
    def post(self, request):
        form = TournamentForm(request.POST)
        if form.is_valid():
            form.instance.organizer = request.user
            form.save()
            return redirect('home')

        return render(request, self.template_name, {'form': form})


class TournamentsView(View):
    template_name = 'tournaments/tournaments.html'

    def get(self, request):
        tournaments = Tournament.objects.all()
        return render(request, self.template_name, {'tournaments': tournaments})


class TournamentView(View):
    template_name = 'tournament/tournament.html'

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        location = get_object_or_404(Location, location_id=tournament.location_id)
        user = request.user
        today = datetime.now().date()

        context = {
            'tournament': tournament,
            'location': location,
            'user': user,
            'edit_delete_permission': user.is_authenticated and
                                      user.has_perm(f'tournaments.edit_delete_tournaments_{tournament_id}'),
            'time_over': tournament.registration_deadline < today,
            'can_read_participants': user.has_perm('tournaments.read_participants'),
            'can_participate': user.has_perm('tournaments.can_participate')
        }

        return render(request, self.template_name, context)


class TournamentEditView(View):
    template_name = 'edit_tournament/edit_tournament.html'

    def get(self, request, tournament_id):
        if not request.user.has_perm(f'tournaments.edit_delete_tournaments_{tournament_id}'):
            raise PermissionDenied

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        form = TournamentEditForm(instance=tournament)

        return render(request, self.template_name, {'form': form, 'tournament': tournament})

    def post(self, request, tournament_id):
        if not request.user.has_perm(f'tournaments.edit_delete_tournaments_{tournament_id}'):
            raise PermissionDenied

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        form = TournamentEditForm(request.POST, instance=tournament)

        if form.is_valid():
            form.save()
            return redirect('tournament', tournament_id)

        return render(request, self.template_name, {'form': form, 'tournament': tournament})


class TournamentDeleteView(View):
    template_name = 'delete_tournament/delete_tournament.html'

    def get(self, request, tournament_id):
        if not request.user.has_perm(f'tournaments.edit_delete_tournaments_{tournament_id}'):
            raise PermissionDenied

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        return render(request, self.template_name, {'tournament': tournament})

    def post(self, request, tournament_id):
        if not request.user.has_perm(f'tournaments.edit_delete_tournaments_{tournament_id}'):
            raise PermissionDenied

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        tournament.delete()
        return redirect('tournaments')


class TournamentRegisterView(View):
    template_name = 'register_tournament/register_tournament.html'
    template_name2 = 'tournament/tournament.html'

    @method_decorator(permission_required('tournaments.can_participate', raise_exception=True))
    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        location = get_object_or_404(Location, location_id=tournament.location_id)
        user = request.user
        today = datetime.now().date()

        context = {
            'tournament': tournament,
            'location': location,
            'user': user,
            'edit_permission': False,
            'error': 'You have been registered.',
            'can_not_register': tournament.registration_deadline < today,
            'can_read_participants': user.has_perm('tournaments.read_participants'),
            'can_participate': user.has_perm('tournaments.can_participate')
        }

        if Participant.objects.filter(user_id=user.user_id, tournament_id=tournament.tournament_id).exists():
            return render(request, self.template_name2, context)

        return render(request, self.template_name, {'tournament': tournament})

    @method_decorator(permission_required('tournaments.can_participate', raise_exception=True))
    def post(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        user = request.user

        if not Participant.objects.filter(user_id=user.user_id, tournament_id=tournament.tournament_id).exists():
            Participant.objects.create(user_id=user.user_id, tournament_id=tournament.tournament_id)
            return redirect('tournament', tournament_id)


class TournamentParticipantsView(View):
    template_name = 'participants/participants.html'

    @method_decorator(permission_required('tournaments.read_participants', raise_exception=True))
    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)

        users = Participant.objects.filter(tournament_id=tournament.tournament_id)
        set_participants = []

        for el in users:
            set_participants.append(CustomUser.objects.filter(user_id=el.user_id))

        return render(request, self.template_name, {'set_participants': set_participants})

