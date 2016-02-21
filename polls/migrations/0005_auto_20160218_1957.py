# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20160218_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='c_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 18, 16, 57, 9, 457165, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_pub_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 18, 16, 57, 9, 454864, tzinfo=utc), verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_rating',
            field=models.IntegerField(verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433'),
        ),
    ]
