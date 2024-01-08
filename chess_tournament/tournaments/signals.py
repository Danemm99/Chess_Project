from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission, ContentType
from tournaments.models import Tournament


@receiver(post_save, sender=Tournament)
def grant_edit_permissions(sender, instance, created, **kwargs):
    if created:
        organizer = instance.organizer
        edit_delete_tournaments_permission = Permission.objects.get_or_create(
            codename=f'edit_delete_tournaments_{instance.tournament_id}',
            name='Edit/delete',
            content_type=ContentType.objects.get_for_model(Tournament),
        )
        organizer.user_permissions.add(edit_delete_tournaments_permission[0])
