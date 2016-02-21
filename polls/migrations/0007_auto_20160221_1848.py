# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20160219_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='c_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 21, 15, 48, 35, 502869, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 21, 15, 48, 35, 500646, tzinfo=utc), verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_rating',
            field=models.IntegerField(default=0, verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433'),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_year_creation',
            field=models.IntegerField(verbose_name='\u0413\u043e\u0434 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2016, 2, 21)),
        ),
    ]
