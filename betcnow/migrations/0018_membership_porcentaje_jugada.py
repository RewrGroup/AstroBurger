# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 03:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betcnow', '0017_auto_20170301_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='porcentaje_jugada',
            field=models.FloatField(default=0.05),
            preserve_default=False,
        ),
    ]
