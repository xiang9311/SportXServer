# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0016_auto_20160530_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblbriefuser',
            name='hadReadMessage',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
