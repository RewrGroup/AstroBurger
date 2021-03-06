# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betcnow', '0023_jugada_premio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='miembro_hasta',
            new_name='valid_thru',
        ),
        migrations.AlterField(
            model_name='jugada',
            name='premio',
            field=models.CharField(blank=True, choices=[('1', '350pts'), ('2', '25pts'), ('3', '15pts'), ('4', '0.0025Btc+10pts')], default='', max_length=30),
        ),
    ]
