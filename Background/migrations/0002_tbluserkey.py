# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblUserKey',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('userKey', models.CharField(max_length=30)),
                ('outOfDateTime', models.DateTimeField()),
                ('user', models.ForeignKey(to='Background.TblBriefUser')),
            ],
        ),
    ]
