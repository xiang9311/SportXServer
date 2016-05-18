# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0002_tbluserkey'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblRongyunToken',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='tblbriefuser',
            name='userPW',
            field=models.CharField(max_length=36),
        ),
        migrations.AlterField(
            model_name='tbluserkey',
            name='userKey',
            field=models.CharField(max_length=36),
        ),
        migrations.AddField(
            model_name='tblrongyuntoken',
            name='user',
            field=models.ForeignKey(to='Background.TblBriefUser'),
        ),
    ]
