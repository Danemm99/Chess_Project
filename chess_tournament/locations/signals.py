# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import Permission, ContentType
# from locations.models import Location
# from users.models import CustomUser
#
#
# @receiver(post_save, sender=CustomUser)
# def add_location_permissions(sender, instance, created, **kwargs):
#     if created and instance.role == 'coach':
#         content_type_location = ContentType.objects.get_for_model(Location)
#
#         add_location_permission, created = Permission.objects.get_or_create(
#             codename='add_location',
#             name='Can add location',
#             content_type=content_type_location,
#         )
#
#         instance.user_permissions.add(add_location_permission)
