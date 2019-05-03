# Generated by Django 2.2 on 2019-05-03 00:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friends',
            unique_together={('inviter', 'target')},
        ),
        migrations.AlterUniqueTogether(
            name='invite',
            unique_together={('target', 'inviter')},
        ),
    ]
