# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-31 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visuals', '0005_auto_20180906_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='visual',
            name='website',
            field=models.TextField(blank=True),
        ),
    ]