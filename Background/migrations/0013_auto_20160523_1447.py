# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0012_auto_20160523_1125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tblliketrend',
            old_name='createUser',
            new_name='likeUser',
        ),
    ]
