# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20160218_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='f_discription',
            field=models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_name',
            field=models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_pub_date',
            field=models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='film',
            name='f_year_creation',
            field=models.DateField(verbose_name='\u0413\u043e\u0434 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f'),
        ),
    ]
