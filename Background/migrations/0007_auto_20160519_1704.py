# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0006_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblbriefuser',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='tblbriefuser',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
