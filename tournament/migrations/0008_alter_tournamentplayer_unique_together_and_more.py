# Generated by Django 5.1.1 on 2024-10-19 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0007_merge_20241019_0028'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tournamentplayer',
            unique_together={('player', 'tournament')},
        ),
        migrations.RemoveField(
            model_name='tournamentplayer',
            name='joined_at',
        ),
    ]
