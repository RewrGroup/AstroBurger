# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-06 03:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betcnow', '0031_auto_20170504_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpsYCookies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elemento', models.CharField(max_length=100)),
            ],
        ),
    ]
