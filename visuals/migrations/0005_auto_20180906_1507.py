# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-06 15:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visuals', '0004_visualimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visual',
            options={'ordering': ['-date_updated']},
        ),
    ]
