# Generated by Django 4.1 on 2024-01-14 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20240107_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images_users/%Y/%m/%d/'),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('follower', 'target_user')},
        ),
    ]
