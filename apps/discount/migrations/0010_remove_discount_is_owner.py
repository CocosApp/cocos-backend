# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-05-14 22:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0009_discount_promotion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='is_owner',
        ),
    ]