# Generated by Django 2.2 on 2019-05-02 03:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0004_auto_20190501_0546'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orginviteinviter', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orginvitetarget', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
