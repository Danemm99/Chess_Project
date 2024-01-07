from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from tournaments.models import Comment, Tournament
from .forms import CommentForm


class TournamentCommentsView(View):
    template_name = 'comments/tournament_comments.html'

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
        comments = Comment.objects.filter(tournament=tournament, parent_comment=None)
        form = CommentForm()

        return render(request, self.template_name, {'user': request.user, 'tournament': tournament, 'comments': comments, 'form': form})

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

        return redirect('tournament_comments', tournament_id)


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

        return redirect('tournament_comments', tournament_id)
