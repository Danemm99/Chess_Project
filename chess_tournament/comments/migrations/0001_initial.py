# Generated by Django 4.1 on 2023-12-04 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('parent_comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.comment')),
            ],
        ),
    ]
