# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0007_auto_20160519_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblbriefuser',
            name='userPhone',
            field=models.CharField(db_index=True, max_length=13),
        ),
    ]
