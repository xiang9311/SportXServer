# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0014_auto_20160523_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblbriefgym',
            name='meituan_price',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblbriefgym',
            name='price',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
