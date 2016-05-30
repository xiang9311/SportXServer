# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0015_auto_20160530_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblgyminfo',
            name='gym',
            field=models.ForeignKey(to='Background.TblBriefGym'),
        ),
    ]
