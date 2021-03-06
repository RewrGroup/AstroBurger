# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-04 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betcnow', '0030_auto_20170327_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='pote',
            name='demo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='jugada',
            name='premio',
            field=models.CharField(blank=True, choices=[('1', '160 pts'), ('2', '40 pts'), ('3', '20 pts'), ('4', '0.0025Btc + 10pts')], default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='pote',
            name='valor_jugada',
            field=models.FloatField(default=0.0),
        ),
    ]
