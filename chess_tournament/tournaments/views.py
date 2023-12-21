from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TournamentForm
from .models import Tournament, Participant
from locations.models import Location
from users.models import CustomUser
from datetime import datetime
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


content_type = ContentType.objects.get_for_model(Tournament)
content_type2 = ContentType.objects.get_for_model(Participant)

permission, created = Permission.objects.get_or_create(
    codename='create-tournament',
    name='Can create',
    content_type=content_type,
)

permission2, created2 = Permission.objects.get_or_create(
    codename='can-participate',
    name='Can participate',
    content_type=content_type2,
)

permission3, created3 = Permission.objects.get_or_create(
    codename='read-participants',
    name='Read participants',
    content_type=content_type2,
)

permission4, created4 = Permission.objects.get_or_create(
    codename='edit-delete-tournaments',
    name='Edit and delete tournaments',
    content_type=content_type,
)

coach_users = CustomUser.objects.filter(role='coach')
participants_users = CustomUser.objects.filter(role='participant')

permission.user_set.set(coach_users)
permission2.user_set.set(participants_users)
permission3.user_set.set(coach_users)
permission4.user_set.set(coach_users)


class TournamentFormView(View):
    template_name = 'tournament_form/tournament_form.html'

    def get(self, request):
        form = TournamentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TournamentForm(request.POST)
        if form.is_valid():
            if request.user.has_perm('tournaments.create-tournament'):
                form.instance.organizer = request.user
                form.save()
                return redirect('home')
            else:
                error_message = "You are not allowed to create tournaments."
                return render(request, self.template_name, {'form': form, 'error': error_message})

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
        organizer_user = CustomUser.objects.get(user_id=tournament.organizer_id)
        user = request.user
        today = datetime.now().date()

        context = {
            'tournament': tournament,
            'location': location,
            'user': user,
            'edit_delete_permission': user.is_authenticated and
                                      user.has_perm('tournaments.edit-delete-tournaments') and
                                      user.user_id == organizer_user.user_id,
            'time_over': tournament.registration_deadline < today,
            'can_read_participants': user.has_perm('tournaments.read-participants'),
            'can_participate': user.has_perm('tournaments.can-participate')
        }

        return render(request, self.template_name, context)


class TournamentEditView(View):
    template_name = 'edit_tournament/edit_tournament.html'

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        form = TournamentForm(instance=tournament)
        return render(request, self.template_name, {'form': form, 'tournament': tournament})

    def post(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        form = TournamentForm(request.POST, instance=tournament)

        if form.is_valid():
            form.save()
            return redirect('tournament', tournament_id)

        return render(request, self.template_name, {'form': form, 'tournament': tournament})


class TournamentDeleteView(View):
    template_name = 'delete_tournament/delete_tournament.html'

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        return render(request, self.template_name, {'tournament': tournament})

    def post(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        tournament.delete()
        return redirect('tournaments')


class TournamentRegisterView(View):
    template_name = 'register_tournament/register_tournament.html'
    template_name2 = 'tournament/tournament.html'

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
            'can_read_participants': user.has_perm('tournaments.read-participants'),
            'can_participate': user.has_perm('tournaments.can-participate')
        }

        if Participant.objects.filter(user_id=user.user_id, tournament_id=tournament.tournament_id).exists():
            return render(request, self.template_name2, context)

        return render(request, self.template_name, {'tournament': tournament})

    def post(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        user = request.user

        if not Participant.objects.filter(user_id=user.user_id, tournament_id=tournament.tournament_id).exists():
            Participant.objects.create(user_id=user.user_id, tournament_id=tournament.tournament_id)
            return redirect('tournament', tournament_id)


class TournamentParticipantsView(View):
    template_name = 'participants/participants.html'

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)

        users = Participant.objects.filter(tournament_id=tournament.tournament_id)
        set_participants = []

        for el in users:
            set_participants.append(CustomUser.objects.filter(user_id=el.user_id))

        return render(request, self.template_name, {'set_participants': set_participants})

