# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0005_auto_20160218_1957'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, blank=True)),
                ('key_expires', models.DateTimeField(default=datetime.date(2016, 2, 19))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User profiles',
            },
        ),
        migrations.AlterField(
            model_name='comment',
            name='c_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 19, 9, 46, 15, 180261, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 19, 9, 46, 15, 177990, tzinfo=utc), verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438'),
        ),
    ]
