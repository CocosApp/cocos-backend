# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-01-18 19:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_enable', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='discount', verbose_name='Imagen')),
            ],
            options={
                'verbose_name_plural': 'Tarjetas',
                'verbose_name': 'Tarjeta',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_enable', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('porc', models.FloatField(blank=True, null=True, verbose_name='Porcentaje')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Precio')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='discount', verbose_name='Imagen')),
                ('terms_condition', models.TextField(blank=True, max_length=100, null=True, verbose_name='Terminos y condiciones')),
                ('descrip', models.TextField(blank=True, max_length=100, null=True, verbose_name='Descripcion')),
                ('is_owner', models.BooleanField(default=True)),
                ('card', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='discount.Card', verbose_name='Tarjeta')),
            ],
            options={
                'verbose_name_plural': 'Descuentos',
                'verbose_name': 'Descuento',
                'ordering': ['name'],
            },
        ),
    ]
