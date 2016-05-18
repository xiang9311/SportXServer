# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TblAllEquipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('equipmentType', models.IntegerField()),
                ('createTime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TblBriefGym',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('gymName', models.CharField(max_length=30)),
                ('gymAvatar', models.URLField()),
                ('place', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('gymIntro', models.CharField(max_length=500)),
                ('createTime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TblBriefUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('userName', models.CharField(max_length=30)),
                ('userPhone', models.CharField(max_length=13)),
                ('userPW', models.CharField(max_length=30)),
                ('userCover', models.URLField()),
                ('userSex', models.BooleanField()),
                ('userSign', models.CharField(max_length=30)),
                ('xMoney', models.IntegerField()),
                ('signTime', models.DateTimeField()),
                ('follow', models.ManyToManyField(to='Background.TblBriefUser')),
            ],
        ),
        migrations.CreateModel(
            name='TblCommentMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('content', models.CharField(max_length=200)),
                ('toUserId', models.IntegerField()),
                ('createTime', models.DateTimeField()),
                ('createUser', models.ForeignKey(to='Background.TblBriefUser')),
            ],
        ),
        migrations.CreateModel(
            name='TblCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('week', models.IntegerField()),
                ('fromHour', models.IntegerField()),
                ('fromMinite', models.IntegerField()),
                ('toHour', models.IntegerField()),
                ('toMinite', models.IntegerField()),
                ('createTime', models.DateTimeField()),
                ('gym', models.ForeignKey(to='Background.TblBriefGym')),
            ],
        ),
        migrations.CreateModel(
            name='TblEverFollow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('followedUserId', models.IntegerField()),
                ('createUserId', models.IntegerField()),
                ('followTime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TblGymCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('cardType', models.IntegerField()),
                ('price', models.FloatField()),
                ('createTime', models.DateTimeField()),
                ('gym', models.ForeignKey(to='Background.TblBriefGym')),
            ],
        ),
        migrations.CreateModel(
            name='TblGymEquipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('equipmentType', models.IntegerField()),
                ('eIntro', models.CharField(max_length=100)),
                ('createTime', models.DateTimeField()),
                ('equipment', models.ForeignKey(to='Background.TblAllEquipment')),
                ('gym', models.ForeignKey(to='Background.TblBriefGym')),
            ],
        ),
        migrations.CreateModel(
            name='TblGyminfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('image', models.URLField()),
                ('imageOrder', models.IntegerField()),
                ('createTime', models.DateTimeField()),
                ('gym', models.ForeignKey(to='Background.TblGymCard')),
            ],
        ),
        migrations.CreateModel(
            name='TblLikeTrend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('createTime', models.DateTimeField()),
                ('createUser', models.ForeignKey(to='Background.TblBriefUser')),
            ],
        ),
        migrations.CreateModel(
            name='TblSearchKeywords',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('keyword', models.CharField(max_length=100)),
                ('usedTimes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TblTrend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('content', models.CharField(max_length=30)),
                ('likeCount', models.IntegerField()),
                ('commentCount', models.IntegerField()),
                ('createTime', models.DateTimeField()),
                ('createUser', models.ForeignKey(to='Background.TblBriefUser')),
                ('gym', models.ForeignKey(to='Background.TblBriefGym')),
            ],
        ),
        migrations.CreateModel(
            name='TblTrendComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('comment', models.CharField(max_length=300)),
                ('toUserId', models.IntegerField()),
                ('commentTime', models.DateTimeField()),
                ('createUser', models.ForeignKey(to='Background.TblBriefUser')),
                ('gym', models.ForeignKey(to='Background.TblBriefGym')),
                ('trend', models.ForeignKey(to='Background.TblTrend')),
            ],
        ),
        migrations.CreateModel(
            name='TblTrendImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('url', models.URLField()),
                ('priority', models.IntegerField()),
                ('createTime', models.DateTimeField()),
                ('createUser', models.ForeignKey(to='Background.TblBriefUser')),
                ('trend', models.ForeignKey(to='Background.TblTrend')),
            ],
        ),
        migrations.CreateModel(
            name='TblXMoneyLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('xMoneyChanged', models.IntegerField()),
                ('reason', models.CharField(max_length=30)),
                ('createTime', models.DateTimeField()),
                ('createUser', models.ForeignKey(to='Background.TblBriefUser')),
            ],
        ),
        migrations.AddField(
            model_name='tblliketrend',
            name='trend',
            field=models.ForeignKey(to='Background.TblTrend'),
        ),
        migrations.AddField(
            model_name='tblcommentmessage',
            name='toTrend',
            field=models.ForeignKey(to='Background.TblTrend'),
        ),
    ]
