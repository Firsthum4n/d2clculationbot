# Generated by Django 5.1.2 on 2024-12-28 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='custom_user',
            options={'verbose_name_plural': 'Users'},
        ),
    ]
