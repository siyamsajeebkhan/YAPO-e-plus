# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_actor_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]