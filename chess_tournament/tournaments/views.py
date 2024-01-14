from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TournamentForm, TournamentEditForm, CommentForm
from .models import Tournament, Participant, Comment
from locations.models import Location
from users.models import CustomUser
from datetime import datetime
from django.core.exceptions import PermissionDenied
from locations.views import PermissionMixin


class PermissionTournamentMixin:
    @staticmethod
    def check_tournament_permission(request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        organizer_user = CustomUser.objects.get(user_id=tournament.organizer_id)

        if not request.user.user_id == organizer_user.user_id:
            raise PermissionDenied


class TournamentFormView(PermissionMixin, View):
    template_name = 'tournament_form/tournament_form.html'

    def get(self, request):
        self.check_coach_permission(request)

        form = TournamentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        self.check_coach_permission(request)

        form = TournamentForm(request.POST, request.FILES)
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
        organizer_user = CustomUser.objects.get(user_id=tournament.organizer_id)
        user = request.user
        today = datetime.now().date()

        context = {
            'tournament': tournament,
            'location': location,
            'user': user,
            'edit_delete_permission': user.is_authenticated and user.user_id == organizer_user.user_id,
            'time_over': tournament.registration_deadline < today,
            'can_read_participants': user.groups.filter(name='Coaches').exists(),
            'can_participate': user.groups.filter(name='Participants').exists()
        }

        return render(request, self.template_name, context)


class TournamentEditView(PermissionTournamentMixin, View):
    template_name = 'edit_tournament/edit_tournament.html'

    def get(self, request, tournament_id):
        self.check_tournament_permission(request, tournament_id)

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        form = TournamentEditForm(instance=tournament)

        return render(request, self.template_name, {'form': form, 'tournament': tournament})

    def post(self, request, tournament_id):
        self.check_tournament_permission(request, tournament_id)

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        form = TournamentEditForm(request.POST, request.FILES, instance=tournament)

        if form.is_valid():
            form.save()
            return redirect('tournament', tournament_id)

        return render(request, self.template_name, {'form': form, 'tournament': tournament})


class TournamentDeleteView(PermissionTournamentMixin, View):
    template_name = 'delete_tournament/delete_tournament.html'

    def get(self, request, tournament_id):
        self.check_tournament_permission(request, tournament_id)

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        return render(request, self.template_name, {'tournament': tournament})

    def post(self, request, tournament_id):
        self.check_tournament_permission(request, tournament_id)

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        tournament.delete()
        return redirect('tournaments')


class TournamentRegisterView(PermissionMixin, View):
    template_name = 'register_tournament/register_tournament.html'
    template_name2 = 'tournament/tournament.html'

    def get(self, request, tournament_id):
        self.check_participant_permission(request)

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
            'can_read_participants': user.groups.filter(name='Coaches').exists(),
            'can_participate': user.groups.filter(name='Participants').exists()
        }

        if Participant.objects.filter(user_id=user.user_id, tournament_id=tournament.tournament_id).exists():
            return render(request, self.template_name2, context)

        return render(request, self.template_name, {'tournament': tournament})

    def post(self, request, tournament_id):
        self.check_participant_permission(request)

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        user = request.user

        if not Participant.objects.filter(user_id=user.user_id, tournament_id=tournament.tournament_id).exists():
            Participant.objects.create(user_id=user.user_id, tournament_id=tournament.tournament_id)
            return redirect('tournament', tournament_id)


class TournamentParticipantsView(PermissionMixin, View):
    template_name = 'participants/participants.html'

    def get(self, request, tournament_id):
        self.check_coach_permission(request)

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)

        users = Participant.objects.filter(tournament_id=tournament.tournament_id)
        set_participants = []

        for el in users:
            set_participants.append(CustomUser.objects.filter(user_id=el.user_id))

        return render(request, self.template_name, {'set_participants': set_participants})


class TournamentCommentsView(View):
    template_name = 'comments/tournament_comments.html'

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        comments = Comment.objects.filter(tournament=tournament, parent_comment=None)
        form = CommentForm()

        return render(request, self.template_name, {
            'user': request.user,
            'tournament': tournament,
            'comments': comments,
            'form': form
        })

    def post(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        form = CommentForm(request.POST)

        if form.is_valid():
            user = request.user
            content = form.cleaned_data['content']
            parent_comment_id = form.cleaned_data.get('parent_comment_id')

            parent_comment = None
            if parent_comment_id:
                parent_comment = get_object_or_404(Comment, comment_id=parent_comment_id)

            Comment.objects.create(user=user, tournament=tournament, content=content, parent_comment=parent_comment)

        return redirect('tournament-comments', tournament_id)


class ReplyCommentView(View):
    template_name = 'comments/reply_comment.html'

    def get(self, request, tournament_id, comment_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        parent_comment = get_object_or_404(Comment, comment_id=comment_id)
        form = CommentForm()

        return render(request, self.template_name,
                      {
                          'tournament': tournament,
                          'parent_comment': parent_comment,
                          'form': form,
                      })

    def post(self, request, tournament_id, comment_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        parent_comment = get_object_or_404(Comment, comment_id=comment_id)

        form = CommentForm(request.POST)

        if form.is_valid():
            user = request.user
            content = form.cleaned_data['content']

            Comment.objects.create(user=user, tournament=tournament, content=content, parent_comment=parent_comment)

        return redirect('tournament-comments', tournament_id)

