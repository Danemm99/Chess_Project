from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import TournamentForm, TournamentEditForm, CommentForm
from .models import Tournament, Participant, Comment
from locations.models import Location
from users.models import CustomUser, Subscription
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


class SubscriptionMixin:
    @staticmethod
    def check_subscription(request, user_id):
        if Subscription.objects.filter(follower_id=request.user.user_id, target_user_id=user_id).exists():
            return True


class ParticipantsCheckMixin:
    @staticmethod
    def participants_check(tournament_id, participant_id):
        participated = False
        participants = Participant.objects.filter(tournament_id=tournament_id)
        for el in participants:
            if el.user_id == participant_id:
                participated = True

        if CustomUser.objects.filter(user_id=participant_id).first().role != 'participant' or not participated:
            raise PermissionDenied


class CommentatorsCheckMixin:
    @staticmethod
    def commentators_check(tournament_id, commentator_id):
        commentator = False
        commentators = Comment.objects.filter(tournament_id=tournament_id)
        for el in commentators:
            if el.user_id == commentator_id:
                commentator = True

        if not commentator:
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
        participants = []
        res = []

        for tournament in tournaments:
            participants.append(Participant.objects.filter(tournament_id=tournament.tournament_id).count())

        for i in range(len(tournaments)):
            res.append(tuple([participants[i], tournaments[i]]))

        return render(request, self.template_name, {
            'tournaments': tournaments,
            'participants': participants,
            'res': res
        })


class TournamentView(View):
    template_name = 'tournament/tournament.html'

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        location = get_object_or_404(Location, location_id=tournament.location_id)
        organizer_user = CustomUser.objects.get(user_id=tournament.organizer_id)
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        comments = Comment.objects.filter(tournament=tournament, parent_comment=None)
        form = CommentForm()
        user = request.user
        today = datetime.now().date()

        context = {
            'tournament': tournament,
            'location': location,
            'user': user,
            'edit_delete_permission': user.is_authenticated and user.user_id == organizer_user.user_id,
            'time_over': tournament.registration_deadline < today,
            'can_read_participants': user.groups.filter(name='Coaches').exists(),
            'can_participate': user.groups.filter(name='Participants').exists(),
            'comments': comments,
            'form': form
        }

        return render(request, self.template_name, context)

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

        return redirect('tournament', tournament_id)


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
        comments = Comment.objects.filter(tournament=tournament, parent_comment=None)
        form = CommentForm()
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
            'can_participate': user.groups.filter(name='Participants').exists(),
            'comments': comments,
            'form': form
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

        queries = []
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        participants_objects = Participant.objects.filter(tournament_id=tournament.tournament_id)
        participants = []
        res = []

        for el in participants_objects:
            queries.append(CustomUser.objects.filter(user_id=el.user_id))

        if len(queries) != 0:
            participants = queries[0]
            for query in queries[1:]:
                participants = participants.union(query)

        for participant in participants:
            res.append(tuple([participant,
                              Subscription.objects.filter(target_user_id=participant.user_id).count(),
                              Subscription.objects.filter(follower_id=participant.user_id).count()]))

        return render(request, self.template_name, {
            'tournament': tournament,
            'res': res
        })


class TournamentParticipantView(PermissionMixin, View, ParticipantsCheckMixin):
    template_name = 'participant/participant.html'

    def get(self, request, tournament_id, participant_id):
        self.participants_check(tournament_id, participant_id)

        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        participant = CustomUser.objects.filter(user_id=participant_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        context = {
            'participant': participant,
            'can_unfollow': Subscription.objects.filter(follower_id=current_user.user_id,
                                                        target_user_id=participant.user_id).first(),
            'tournament': tournament
        }

        return render(request, self.template_name, context)


class ParticipantFollowView(View, ParticipantsCheckMixin, SubscriptionMixin):
    template_name = 'follow_tournament/follow_tournament.html'

    def get(self, request, tournament_id, participant_id):
        self.participants_check(tournament_id, participant_id)

        if self.check_subscription(request, participant_id):
            raise PermissionDenied

        participant = get_object_or_404(CustomUser, user_id=participant_id)
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)

        return render(request, self.template_name, {'participant': participant, 'tournament': tournament})

    def post(self, request, tournament_id, participant_id):
        participant = CustomUser.objects.filter(user_id=participant_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        Subscription.objects.create(follower_id=current_user.user_id, target_user_id=participant.user_id)

        return redirect('participant-tournament', tournament_id, participant_id)


class ParticipantUnfollowView(View, ParticipantsCheckMixin, SubscriptionMixin):
    template_name = 'unfollow_tournament/unfollow_tournament.html'

    def get(self, request, tournament_id, participant_id):
        self.participants_check(tournament_id, participant_id)

        if not self.check_subscription(request, participant_id):
            raise PermissionDenied

        participant = get_object_or_404(CustomUser, user_id=participant_id)
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        return render(request, self.template_name, {'participant': participant, 'tournament': tournament})

    def post(self, request, tournament_id, participant_id):
        participant = CustomUser.objects.filter(user_id=participant_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        subscription = Subscription.objects.filter(follower_id=current_user.user_id,
                                                   target_user_id=participant.user_id)
        subscription.delete()

        return redirect('participant-tournament', tournament_id, participant_id)


class CommentatorView(View, CommentatorsCheckMixin):
    template_name = 'comments/commentator.html'

    def get(self, request, tournament_id, commentator_id):
        if request.user.user_id == commentator_id:
            return redirect('home')

        self.commentators_check(tournament_id, commentator_id)

        commentator = CustomUser.objects.filter(user_id=commentator_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        context = {
            'tournament': tournament,
            'commentator': commentator,
            'can_unfollow': Subscription.objects.filter(follower_id=current_user.user_id,
                                                        target_user_id=commentator.user_id).first()
        }

        return render(request, self.template_name, context)


class CommentFollowView(View, CommentatorsCheckMixin, SubscriptionMixin):
    template_name = 'comments/comment_follow_tournament.html'

    def get(self, request, tournament_id, commentator_id):
        if request.user.user_id == commentator_id:
            raise PermissionDenied

        self.commentators_check(tournament_id, commentator_id)

        if self.check_subscription(request, commentator_id):
            raise PermissionDenied

        commentator = get_object_or_404(CustomUser, user_id=commentator_id)
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        return render(request, self.template_name, {'commentator': commentator, 'tournament': tournament})

    def post(self, request, tournament_id, commentator_id):
        commentator = CustomUser.objects.filter(user_id=commentator_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        Subscription.objects.create(follower_id=current_user.user_id, target_user_id=commentator.user_id)

        return redirect('commentator-tournament', tournament_id, commentator_id)


class CommentUnfollowView(View, CommentatorsCheckMixin, SubscriptionMixin):
    template_name = 'comments/comment_unfollow_tournament.html'

    def get(self, request, tournament_id, commentator_id):
        if request.user.user_id == commentator_id:
            raise PermissionDenied

        self.commentators_check(tournament_id, commentator_id)

        if not self.check_subscription(request, commentator_id):
            raise PermissionDenied

        commentator = get_object_or_404(CustomUser, user_id=commentator_id)
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        return render(request, self.template_name, {'commentator': commentator, 'tournament': tournament})

    def post(self, request, tournament_id, commentator_id):
        commentator = CustomUser.objects.filter(user_id=commentator_id).first()
        current_user = CustomUser.objects.filter(user_id=request.user.user_id).first()
        subscription = Subscription.objects.filter(follower_id=current_user.user_id,
                                                   target_user_id=commentator.user_id)
        subscription.delete()

        return redirect('commentator-tournament', tournament_id, commentator_id)


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

        return redirect('tournament', tournament_id)

