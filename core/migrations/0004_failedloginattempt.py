# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20170904_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='FailedLoginAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ip', models.GenericIPAddressField()),
                ('user_exists', models.BooleanField()),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
