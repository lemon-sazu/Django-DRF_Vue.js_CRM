# Generated by Django 3.2.4 on 2021-06-28 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_auto_20210627_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='max_client',
            new_name='max_clients',
        ),
    ]
