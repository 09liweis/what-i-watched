# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-31 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visuals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visual',
            name='release_date',
            field=models.TextField(blank=True),
        ),
    ]
