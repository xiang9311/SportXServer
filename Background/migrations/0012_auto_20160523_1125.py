# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0011_auto_20160523_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbltrend',
            name='content',
            field=models.CharField(null=True, max_length=30),
        ),
    ]
