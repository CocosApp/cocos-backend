# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-02-28 00:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0005_auto_20180207_1707'),
        ('restaurant', '0004_auto_20180214_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('discount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='res_discount', to='discount.Discount')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='res_discount', to='restaurant.Restaurant')),
            ],
            options={
                'verbose_name': 'Restaurante y su descuento',
                'verbose_name_plural': 'Restaurante y sus descuentos',
            },
        ),
        migrations.AddField(
            model_name='restaurant',
            name='discountnew',
            field=models.ManyToManyField(blank=True, null=True, related_name='res', through='restaurant.RestaurantDiscount', to='discount.Discount', verbose_name='Descuentos nuevos'),
        ),
        migrations.AlterUniqueTogether(
            name='restaurantdiscount',
            unique_together=set([('restaurant', 'discount')]),
        ),
    ]