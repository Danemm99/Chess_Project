from django.db import models
from users.models import CustomUser
from tournaments.models import Tournament


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
