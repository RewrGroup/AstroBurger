# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betcnow', '0012_testimonio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonio',
            name='fecha',
            field=models.DateField(blank=True, null=True),
        ),
    ]