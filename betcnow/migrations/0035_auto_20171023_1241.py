# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-23 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betcnow', '0034_auto_20171023_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugada',
            name='premio',
            field=models.CharField(blank=True, choices=[('1', '48 Bitcoin Race points'), ('2', '12 Bitcoin Race points'), ('3', '6 Bitcoin Race points'), ('4', '3 Bitcoin Race points')], default='', max_length=30),
        ),
    ]