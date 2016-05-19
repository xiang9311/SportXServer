# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0004_auto_20160519_1059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tblbriefuser',
            old_name='userCover',
            new_name='userAvatar',
        ),
        migrations.AddField(
            model_name='tblbriefuser',
            name='latitude',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tblbriefuser',
            name='longitude',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
