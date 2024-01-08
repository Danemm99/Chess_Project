from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def add_to_group(sender, instance, created, **kwargs):
    if created:
        role = instance.role

        group_coaches, created = Group.objects.get_or_create(name='Coaches')
        group_participants, created = Group.objects.get_or_create(name='Participants')

        if role == 'coach':
            group_coaches.user_set.add(instance)
        elif role == 'participant':
            group_participants.user_set.add(instance)
