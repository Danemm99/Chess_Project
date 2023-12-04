from django.db import models
from users.models import CustomUser
from tournaments.models import Tournament


class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    unique_participation = models.UniqueConstraint(fields=['user', 'tournament'], name='unique_participation')
