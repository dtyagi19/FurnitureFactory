# Generated by Django 3.1.7 on 2021-03-24 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tableFactory', '0003_auto_20210324_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feet',
            name='length',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='feet',
            name='radius',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='feet',
            name='width',
            field=models.IntegerField(null=True),
        ),
    ]
