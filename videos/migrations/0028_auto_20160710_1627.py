# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-10 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0027_auto_20160708_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='extra_text',
            field=models.TextField(blank=True, default=''),
        ),
    ]