# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20160218_1914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='u_id',
        ),
        migrations.RemoveField(
            model_name='film',
            name='f_id',
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_discription',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_year_creation',
            field=models.DateField(verbose_name=b'year of film creation'),
        ),
        migrations.AlterField(
            model_name='score',
            name='film',
            field=models.ForeignKey(related_name='score_film', to='polls.Film'),
        ),
        migrations.AlterField(
            model_name='score',
            name='value',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='score',
            name='voter',
            field=models.ForeignKey(related_name='score_voter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
