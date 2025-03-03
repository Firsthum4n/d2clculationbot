# Generated by Django 5.1.2 on 2024-12-28 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_heroes_options_alter_players_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroes',
            name='agi_gain',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='heroes',
            name='attack_point',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='heroes',
            name='attack_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='heroes',
            name='int_gain',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='heroes',
            name='str_gain',
            field=models.FloatField(default=0),
        ),
    ]
