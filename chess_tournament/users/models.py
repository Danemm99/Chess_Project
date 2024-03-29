from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superuser')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to='images_users/%Y/%m/%d/', default=None, blank=True, null=True)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    @staticmethod
    def get_by_email(email):
        custom_user = CustomUser.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def get_by_id(user_id):
        custom_user = CustomUser.objects.filter(user_id=user_id).first()
        return custom_user if custom_user else None

    @property
    def is_participant(self):
        return self.role == 'participant'

    @property
    def is_coach(self):
        return self.role == 'coach'

    def __str__(self):
        return f'{self.username}'


class Subscription(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(CustomUser, related_name='follower_id', on_delete=models.CASCADE)
    target_user = models.ForeignKey(CustomUser, related_name='target_user_id', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['follower', 'target_user']
