from django.contrib.auth.models import User
from django.db import models
from django.db.models import *

class Card(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_enable = models.BooleanField(default=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    photo = models.ImageField(upload_to='discount', blank=True, null=True, verbose_name="Imagen")

    class Meta:
        verbose_name_plural = "Tarjetas"
        verbose_name = "Tarjeta"
        ordering = ['name', ]

    def __str__(self):
        return self.name

class Discount(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_enable = models.BooleanField(default=True,verbose_name='¿Está disponible?')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    card =models.ForeignKey(Card,related_name="cards",verbose_name="Tarjeta",blank=True,null=True)
    porc = models.FloatField(verbose_name='Porcentaje',blank=True,null=True)
    price = models.FloatField(verbose_name='Precio',blank=True,null=True)
    promotion = models.CharField(verbose_name='Promocion',blank=True,null=True, max_length=200)
    photo = models.ImageField(upload_to='discount', blank=True, null=True, verbose_name="Imagen")
    terms_condition = models.TextField(max_length=2000, verbose_name='Terminos y condiciones',blank=True,null=True)
    descrip = models.TextField(max_length=1000, verbose_name='Descripcion',blank=True,null=True)
    finished_at = models.DateTimeField(verbose_name='Fecha de vencimiento', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Descuentos"
        verbose_name = "Descuento"
        ordering = ['name', ]

    def __str__(self):
        return self.name