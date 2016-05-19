# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0003_auto_20160518_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbltrendcomment',
            name='toCommentId',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
