# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 23:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betcnow', '0021_pote_fecha_sorteo'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='puntos',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
