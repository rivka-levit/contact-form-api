# Generated by Django 4.2.6 on 2023-10-07 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='is_banned',
        ),
    ]
