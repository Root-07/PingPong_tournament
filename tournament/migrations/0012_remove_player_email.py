# Generated by Django 4.2.16 on 2024-11-13 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0011_remove_match_result_tournament_creator_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='email',
        ),
    ]
