from django.db import models
from locations.models import Location
from users.models import CustomUser


class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    prizes = models.TextField()
    date = models.DateField()
    registration_deadline = models.DateField()
    tournament_image = models.ImageField(upload_to='images_tournaments/%Y/%m/%d/', default=None, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'tournament']


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.parent_comment:
            return f'{self.parent_comment.user.username} - {self.content}'
        elif self.user:
            return f'{self.user.username} - {self.content}'
        else:
            return f'Comment-{self.comment_id}'

    def get_replies(self):
        return Comment.objects.filter(parent_comment=self)
