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
