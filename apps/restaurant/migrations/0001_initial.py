# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-01-18 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_enable', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('ruc', models.CharField(blank=True, max_length=20, null=True, verbose_name='RUC')),
                ('longitude', models.FloatField(verbose_name='Longitud')),
                ('latitude', models.FloatField(verbose_name='Latitud')),
                ('address', models.CharField(max_length=255, verbose_name='Direccion')),
                ('food_letter', models.FileField(blank=True, null=True, upload_to='restaurant_pdf', verbose_name='Carta de comida')),
                ('mobile', models.CharField(blank=True, max_length=100, null=True, verbose_name='Celular 1')),
                ('mobile2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Celular 2')),
                ('photo1', models.ImageField(blank=True, null=True, upload_to='restaurant_pic', verbose_name='Imagen 1')),
                ('photo2', models.ImageField(blank=True, null=True, upload_to='restaurant_pic', verbose_name='Imagen 2')),
                ('photo3', models.ImageField(blank=True, null=True, upload_to='restaurant_pic', verbose_name='Imagen 3')),
                ('discount', models.ManyToManyField(blank=True, null=True, related_name='restaurants', to='discount.Discount', verbose_name='Descuentos')),
            ],
            options={
                'verbose_name_plural': 'Restaurantes',
                'verbose_name': 'Restaurante',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ingresar horario (Ex: De 11am a 4pm)')),
            ],
            options={
                'verbose_name_plural': 'Horarios',
                'verbose_name': 'Horario',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_enable', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nombre del servicio')),
            ],
            options={
                'verbose_name_plural': 'Servicios',
                'verbose_name': 'Servicio',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_enable', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200, verbose_name='Nombre de la sub categoría')),
                ('descrip', models.CharField(max_length=200, verbose_name='Descripción ')),
                ('image', models.ImageField(blank=True, null=True, upload_to='sub_category', verbose_name='Imagen de la sub categoria')),
            ],
            options={
                'verbose_name_plural': 'Sub categorías',
                'verbose_name': 'Sub categoría',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='restaurant',
            name='schedule',
            field=models.ManyToManyField(blank=True, null=True, related_name='schedules', to='restaurant.Schedule', verbose_name='Horario'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='service',
            field=models.ManyToManyField(blank=True, null=True, related_name='services', to='restaurant.Service', verbose_name='Servicios'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='subcategory',
            field=models.ManyToManyField(blank=True, null=True, related_name='sub_categories', to='restaurant.Subcategory', verbose_name='Sub categorias'),
        ),
    ]
