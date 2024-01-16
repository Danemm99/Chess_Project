# Generated by Django 4.1 on 2024-01-14 18:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='tournament_image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images_tournaments/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='participant',
            unique_together={('user', 'tournament')},
        ),
    ]
