# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betcnow', '0003_auto_20170213_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pote',
            name='valor_jugada',
            field=models.FloatField(),
        ),
    ]
