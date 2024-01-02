from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission, ContentType
from tournaments.models import Tournament, Participant
from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def add_tournament_permissions(sender, instance, created, **kwargs):
    if created:
        content_type_tournament = ContentType.objects.get_for_model(Tournament)
        content_type_participant = ContentType.objects.get_for_model(Participant)

        create_tournament_permission, created = Permission.objects.get_or_create(
            codename='create_tournament',
            name='Can create',
            content_type=content_type_tournament,
        )

        can_participate_permission, created = Permission.objects.get_or_create(
            codename='can_participate',
            name='Can participate',
            content_type=content_type_participant,
        )

        read_participants_permission, created = Permission.objects.get_or_create(
            codename='read_participants',
            name='Read participants',
            content_type=content_type_participant,
        )

        if instance.role == 'coach':
            instance.user_permissions.add(
                create_tournament_permission,
                read_participants_permission,
            )

        elif instance.role == 'participant':
            instance.user_permissions.add(can_participate_permission)


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
