# Generated by Django 3.1.7 on 2021-03-24 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tableFactory', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leg',
            old_name='feet',
            new_name='feet_id',
        ),
        migrations.RenameField(
            model_name='table',
            old_name='leg',
            new_name='leg_id',
        ),
    ]
