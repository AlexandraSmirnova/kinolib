# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='superuser_flag',
            field=models.NullBooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='u_id',
            field=models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL),
        ),
    ]
