# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-02-22 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20180222_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='business_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Razón social'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cellphone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Celular'),
        ),
        migrations.AlterField(
            model_name='user',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Comentarios'),
        ),
        migrations.AlterField(
            model_name='user',
            name='ruc',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='RUC'),
        ),
    ]
