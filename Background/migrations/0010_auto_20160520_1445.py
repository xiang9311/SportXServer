# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0009_auto_20160519_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbltrend',
            name='gym',
            field=models.ForeignKey(to='Background.TblBriefGym', null=True),
        ),
    ]
