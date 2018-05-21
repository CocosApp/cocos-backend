from faulthandler import _read_null
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from apps.discount.models import *
from apps.restaurant.models import *

class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        user = self.model(email=email, is_active=True,
                          is_staff=is_staff, is_superuser=is_superuser,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_admin_res = models.BooleanField(default=False, blank=True, verbose_name="¿Es admin de un restaurante?")
    email = models.EmailField(unique=True,verbose_name="Correo")
    first_name = models.CharField(max_length=100,verbose_name='Nombres')
    last_name = models.CharField(max_length=100,verbose_name='Apellidos')
    ruc = models.CharField(max_length=20, verbose_name='RUC',blank=True, null=True)
    business_name = models.CharField(max_length=100,verbose_name='Razón social',blank=True, null=True)
    cellphone = models.CharField(max_length=20,verbose_name='Celular',blank=True, null=True)
    comment = models.TextField(verbose_name='Comentarios',blank=True, null=True)
    picture = models.ImageField(upload_to='user', blank=True, null=True, verbose_name='Foto personal')
    objects = UserManager()
    birthday = models.DateField(blank=True,null=True,verbose_name="Cumpleaños")
    fav_restaurant = models.ManyToManyField(Restaurant, related_name='restaurants',verbose_name="Restaurantes favoritos",
                                            through='UserRestaurant',blank=True, null=True)
    restaurant = models.ManyToManyField(Restaurant, related_name='admrestaurants',verbose_name="Mis restaurantes",
                                            through='UserAdminRestaurant',blank=True, null=True)
    #Restaurants for the admin
    fav_card = models.ManyToManyField(Card,related_name='fav_cards',verbose_name="Tarjetas favoritas",blank=True, null=True)
    is_invited = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=True, verbose_name='Habilitar Usuario')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_facebook =models.BooleanField(default=False)
    is_gmail = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural ="Usuarios"

    def __str__(self):
        obj = self.email+' - '+self.first_name+' '+self.last_name
        return obj


class UserRestaurant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='user_restaurants')
    restaurant = models.ForeignKey(Restaurant, related_name='user_restaurants')
    is_color = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'restaurant')
        verbose_name = "Usuario y su restaurante favorito"
        verbose_name_plural = "Usuarios y sus restaurantes favoritos"

    def __str__(self):
        obj = str(self.id)
        return obj

class UserAdminRestaurant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='user_admrestaurants',verbose_name='Email - nombre completo')
    restaurant = models.ForeignKey(Restaurant, related_name='user_admrestaurants',verbose_name='Nombre de local')
    is_enable= models.BooleanField(default=False,verbose_name='¿Desea aceptar al nuevo usuario?')

    class Meta:
        unique_together = ('user', 'restaurant')
        verbose_name = "Admin y su restaurante"
        verbose_name_plural = "Super Admin y sus restaurantes"

    def __str__(self):
        return self.user.first_name + ' - '+self.user.last_name+' - '+self.restaurant.name
