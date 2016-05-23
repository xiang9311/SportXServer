# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0013_auto_20160523_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbltrend',
            name='content',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
