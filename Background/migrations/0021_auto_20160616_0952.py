# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 09:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Background', '0020_tblbriefuser_geohash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblbriefuser',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='tblbriefuser',
            name='longitude',
        ),
    ]
