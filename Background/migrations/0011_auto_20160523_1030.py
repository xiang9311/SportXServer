# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0010_auto_20160520_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbltrendcomment',
            name='gym',
            field=models.ForeignKey(to='Background.TblBriefGym', null=True),
        ),
        migrations.AlterField(
            model_name='tbltrendcomment',
            name='toCommentId',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='tbltrendcomment',
            name='toUserId',
            field=models.IntegerField(null=True),
        ),
    ]
