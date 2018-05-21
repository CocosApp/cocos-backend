from django.contrib.auth.models import User
from django.db.models import *
from apps.discount.models import *
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Subcategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_enable = models.BooleanField(default=True)
    name = models.CharField(max_length=200, verbose_name="Nombre de la sub categoría")
    descrip = models.CharField(max_length=200,verbose_name="Descripción ")
    image = models.ImageField(upload_to='sub_category', blank=True, null=True, verbose_name="Imagen de la sub categoria")
    priority = models.PositiveIntegerField(verbose_name='Numero de prioridad',blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sub categorías"
        verbose_name = "Sub categoría"
        ordering = ['id', ]

    def __str__(self):
        obj = str(self.id) + '-' + self.name
        return obj

class Service(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_enable = models.BooleanField(default=True)
    name = models.CharField(max_length=200, verbose_name="Nombre del servicio")

    class Meta:
        verbose_name_plural = "Servicios"
        verbose_name = "Servicio"
        ordering = ['name', ]

    def __str__(self):
        return self.name

class Schedule(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, verbose_name="Ingresar horario (Ex: De 11am a 4pm)",blank=True,null=True)

    class Meta:
        verbose_name_plural = "Horarios"
        verbose_name = "Horario"
        ordering = ['name', ]

    def __str__(self):
        return self.name

class Restaurant(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_enable = models.BooleanField(default=True)
    name = models.CharField(max_length=100, verbose_name='Nombre')
    ruc = models.CharField(max_length=20,verbose_name="RUC",blank=True,null=True)
    subcategory = models.ManyToManyField(Subcategory,related_name="sub_categories",verbose_name="Sub categorias",blank=True,null=True)
    longitude = models.FloatField(verbose_name='Longitud')
    latitude = models.FloatField(verbose_name='Latitud')
    address = models.CharField(max_length=255, verbose_name='Direccion')
    schedule =models.ManyToManyField(Schedule,related_name="schedules",verbose_name="Horario",blank=True,null=True)
    discount= models.ManyToManyField(Discount,related_name="restaurants", verbose_name="Descuentos nuevos",blank=True,null=True,
                                        through='RestaurantDiscount')
    food_letter=models.FileField(upload_to='restaurant_pdf',blank=True,null=True,verbose_name="Carta de comida")
    mobile = models.CharField(max_length=100, verbose_name='Celular 1',blank=True,null=True,)
    mobile2 = models.CharField(max_length=100, verbose_name='Celular 2',blank=True,null=True,)
    photo1 = models.ImageField(upload_to='restaurant_pic', blank=True, null=True, verbose_name="Imagen 1")
    photo2 = models.ImageField(upload_to='restaurant_pic', blank=True, null=True, verbose_name="Imagen 2")
    photo3 = models.ImageField(upload_to='restaurant_pic', blank=True, null=True, verbose_name="Imagen 3")
    whatsapp = models.CharField(max_length=100, verbose_name='Whatsapp (Agregar "+51" si es de Perú)',default='',blank=True,null=True)
    facebook = models.CharField(max_length=300, verbose_name='Link de facebook',default='',blank=True,null=True)
    service = models.ManyToManyField(Service,related_name="services", verbose_name="Servicios",blank=True,null=True)
    location = PointField(blank = True, null=True, srid=4326)
    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        self.location = Point(self.longitude, self.latitude)
        super(Restaurant, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Restaurantes"
        verbose_name = "Restaurante"
        ordering = ['name', ]

    def __str__(self):
        obj =  self.name +'-'+ str(self.id)
        return obj

class RestaurantDiscount(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    restaurant = models.ForeignKey(Restaurant, related_name='res_discount')
    discount = models.ForeignKey(Discount,related_name='res_discount')
    is_enable = models.BooleanField(default=True, verbose_name='¿Está disponible?')

    class Meta:
        unique_together = ('restaurant', 'discount')
        verbose_name = "Restaurante y su descuento"
        verbose_name_plural = "Restaurante y sus descuentos"

    def __str__(self):
        return self.restaurant.name + '-' + self.discount.name