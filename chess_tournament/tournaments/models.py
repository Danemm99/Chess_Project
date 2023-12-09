from django.db import models
from locations.models import Location
from users.models import CustomUser


class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    prizes = models.TextField()
    date = models.DateField()
    registration_deadline = models.DateField()


class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    unique_participation = models.UniqueConstraint(fields=['user', 'tournament'], name='unique_participation')


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
