from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    profile_image = models.BinaryField(null=True)
    is_active = models.BooleanField(default=False)

    @staticmethod
    def get_by_email(email):
        custom_user = CustomUser.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def get_by_id(user_id):
        custom_user = CustomUser.objects.filter(user_id=user_id).first()
        return custom_user if custom_user else None


class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(CustomUser, related_name='follower_id', on_delete=models.CASCADE)
    target_user = models.ForeignKey(CustomUser, related_name='target_user_id', on_delete=models.CASCADE)
    unique_subscription = models.UniqueConstraint(fields=['follower', 'target_user'], name='unique_subscription')
