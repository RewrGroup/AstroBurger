# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 01:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betcnow', '0015_auto_20170223_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugada',
            name='fecha_jugada',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]