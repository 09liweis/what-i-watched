# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-21 21:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visuals', '0003_auto_20180222_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisualImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True)),
                ('url', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('visual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visuals.Visual')),
            ],
            options={
                'ordering': ('date_created',),
            },
        ),
    ]
