# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('c_text', models.TextField(max_length=400)),
                ('c_pub_date', models.DateTimeField()),
                ('c_flag', models.NullBooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('f_id', models.IntegerField()),
                ('f_name', models.CharField(max_length=100)),
                ('f_discription', models.CharField(max_length=400)),
                ('f_pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('f_year_creation', models.IntegerField()),
                ('f_rating', models.IntegerField()),
                ('f_flag', models.NullBooleanField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('u_id', models.IntegerField()),
                ('u_name', models.CharField(max_length=100)),
                ('u_sername', models.CharField(max_length=100)),
                ('u_email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('film', models.IntegerField(default=0)),
                ('voter', models.ForeignKey(related_name='Score_Voter', to='polls.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(to='polls.Profile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='film',
            field=models.ForeignKey(to='polls.Film'),
        ),
    ]
