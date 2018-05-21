from django.contrib.auth import authenticate, login
from requests.exceptions import HTTPError
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.message import EmailMessage
from requests.exceptions import HTTPError
from django.template import loader
from django.conf import settings
from rest_framework import serializers
from social.exceptions import AuthCanceled
from apps.restaurant.serializers import RestaurantBasicSerializer, SubCategorySerializer
from rest_framework.serializers import PrimaryKeyRelatedField
from fcm_django.models import FCMDevice
from django.core.mail import send_mail


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name','birthday','is_invited','is_facebook','is_gmail')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class CreateUserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name','ruc','business_name','cellphone','comment')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        is_admin_res = True
        is_enabled = False
        user = User.objects.create(email=validated_data['email'], first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'], ruc =validated_data['ruc'],
                                   business_name =validated_data['business_name'],cellphone =validated_data['cellphone'],
                                   comment=validated_data['comment'] ,is_admin_res=is_admin_res, is_enabled=is_enabled)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

    def send_mail(self):
        msj = "Un nuevo usuario a solicitado la activación de su cuenta  http://backend.appcocos.com/admin/account/useradminrestaurant/"
        send_mail('Afiliación de un restaurante nuevo',
                  '''
                  Nombre del usuario: {} {}
                  Email: {}
                  Celular:{}
                  Mensaje:
                  {}
                  Datos del restaurante: 
                  {}


                  '''.format(self.validated_data["first_name"], self.validated_data["last_name"], self.validated_data["email"],
                             self.validated_data["cellphone"], msj,self.validated_data["comment"]),
                  self.validated_data.get("email"), ['contacto@appcocos.com'], fail_silently=False)

class EmailWebContactSerializer(serializers.Serializer):

    msg = serializers.CharField(error_messages={"blank": "Este campo es obligatorio"})
    full_name = serializers.CharField(error_messages={"blank": "Este campo es obligatorio"})
    email = serializers.EmailField(error_messages={"blank": "Este campo es obligatorio"})

    def send_mail(self):
        send_mail('Una persona se quiere contactar con nosotros',
                  '''
                  Nombre del contacto: {} 
                  Email: {}
                  Mensaje:
                  {}
                  '''.format(self.validated_data["full_name"],self.validated_data["email"],
                             self.validated_data["msg"]),
                  self.validated_data.get("email"), ['contacto@appcocos.com'], fail_silently=False)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={"blank": "Este campo es obligatorio"})
    password = serializers.CharField(error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        self.user_cache = authenticate(email=attrs["email"], password=attrs["password"])
        if not self.user_cache:
            raise serializers.ValidationError("Invalid login")
        elif self.user_cache.is_admin_res == False:
            return attrs
        else:
            raise serializers.ValidationError('User is not client ')


    def get_user(self):
        return self.user_cache

class LoginAdminSerializer(serializers.Serializer):
    email = serializers.EmailField(error_messages={"blank": "Este campo es obligatorio"})
    password = serializers.CharField(error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        self.user_cache = authenticate(email=attrs["email"], password=attrs["password"])
        if not self.user_cache:
            raise serializers.ValidationError("Invalid login")
        elif (self.user_cache.is_admin_res == True) and (self.user_cache.is_enabled == True):
            return attrs
        else:
            raise serializers.ValidationError('User is not admin restaurant or is not actived')

    def get_user(self):
        return self.user_cache


class RetrieveUserSerializer(serializers.ModelSerializer):
    facebook_uid = serializers.SerializerMethodField(read_only=True)
    google_uid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name','birthday','picture','fav_restaurant','fav_card','is_facebook',
             'is_gmail','facebook_uid', 'google_uid')
        read_only_fields = ('id', 'email', 'facebook_uid', 'google_uid')

    def get_facebook_uid(self, obj):
        return obj.social_auth.filter(provider='facebook').first().uid if obj.social_auth.filter(
            provider='facebook').count() > 0 else None

    def get_google_uid(self, obj):
        return obj.social_auth.filter(provider='google-oauth2').first().uid if obj.social_auth.filter(
            provider='google-oauth2').count() > 0 else None

class RestaurantAdminBasicSerializer(serializers.ModelSerializer):

    subcategory = SubCategorySerializer(many=True)

    class Meta:
        model= Restaurant
        fields = ('id','name','subcategory','photo1','discount')

class RetrieveUserAdminSerializer(serializers.ModelSerializer):

    restaurant = RestaurantAdminBasicSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ( 'id', 'email', 'first_name', 'last_name','ruc','cellphone','business_name','birthday','picture','is_admin_res','restaurant')
        read_only_fields = ('id', 'email',)


class FacebookLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(
        error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        request = self.context.get("request")
        self.user_cache = None
        try:
            self.user_cache = request.backend.do_auth(attrs.get("access_token"))
            return attrs
        except HTTPError:
            raise serializers.ValidationError("Invalid token")
        except AuthCanceled:
            raise serializers.ValidationError("Token expired")

    def get_user(self):
        return self.user_cache

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        error_messages={"blank": "Este campo es obligatorio"})
    new_password = serializers.CharField(
        error_messages={"blank": "Este campo es obligatorio"})
    email = serializers.EmailField(
        error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        user = self.context.get("user")
        if attrs.get("email") != user.email:
            raise serializers.ValidationError({"email": "Email mismatch"})
        if not user.check_password(attrs.get("old_password")):
            raise serializers.ValidationError({"password": "Password mismatch"})
        return attrs

    def save(self, **kwargs):
        user = self.context.get("user")
        user.set_password(self.validated_data.get("new_password"))
        user.save()

class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        self.cached_user = User.objects.filter(email=value).first()
        if not self.cached_user:
            raise serializers.ValidationError("The email is not registered")
        return value


class UserFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'picture')


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','is_facebook','is_gmail')

class UpdateUserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','ruc','business_name','cellphone','picture','birthday')


class UpdateUserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('picture',)


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',)

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'picture',)

class SubCategorySerializer2(serializers.ModelSerializer): #Creo esto para que no hay conflictos

    class Meta:
        model = Subcategory
        fields = ('id','name','descrip','image')

class RestaurantBasicSerializer2(serializers.ModelSerializer):#Creo esto para que no hay conflictos

    subcategory = SubCategorySerializer2(many=True)
    user_restaurants = serializers.StringRelatedField(read_only=True,many=True)

    class Meta:
        model= Restaurant
        fields = ('id','name','subcategory','photo1','user_restaurants')

class RestaurantBasicAdminSerializer(serializers.ModelSerializer): #Solo datos para el admin

    subcategory = SubCategorySerializer2(many=True)

    class Meta:
        model = Restaurant
        fields = ('id','name','photo1','subcategory')

class ListFavRestaurantSerializer(serializers.ModelSerializer): #Necesito jalar el id de user-restaurant

    fav_restaurant = RestaurantBasicSerializer2(many=True,read_only=True)

    class Meta:
        model = User
        fields = ['fav_restaurant',]

class CRUDUserRestaurantSerializer(serializers.ModelSerializer):
    restaurant = PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), required=False)

    class Meta:
        model = UserRestaurant
        fields = ('restaurant',)


class RetrieveUserRestaurantSerializer(serializers.ModelSerializer):

    restaurant = RestaurantBasicSerializer(read_only=True, required=False)

    class Meta:
        model = UserRestaurant
        fields = ('id', 'restaurant',)

class CRUDUserAdminRestaurantSerializer(serializers.ModelSerializer):
    restaurant = PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), required=False)

    class Meta:
        model = UserAdminRestaurant
        fields = ('restaurant',)

class RetrieveUserAdminRestaurantSerializer(serializers.ModelSerializer):

    restaurant = RestaurantBasicAdminSerializer(read_only=True, required=False)

    class Meta:
        model = UserAdminRestaurant
        fields = ('id', 'restaurant',)

class FCMDeviceSerializer(serializers.ModelSerializer):
    registration_id = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)

    def validate_registration_id(self, attr):
        user = getattr(self.context.get("request"), "user")
        try:
            if type(eval(attr)).__name__ == 'dict':
                return eval(attr).get('token')
            else:
                raise serializers.ValidationError("Registration id inválido")
        except SyntaxError:
            return attr

    class Meta:
        model = FCMDevice
        fields = ('id', 'user', 'device_id', 'registration_id', 'name', 'type')


class UpdateFCMDeviceSerializer(serializers.ModelSerializer):
    registration_id = serializers.CharField(required=True)
    device_id = serializers.CharField(required=True)

    def validate_device_id(self, attr):
        user = getattr(self.context.get("request"), "user")
        if not self.Meta.model.objects.filter(device_id=attr, user=user).exists():
            raise serializers.ValidationError("El usuario no ha registrado este dispositivo")
        return attr

    class Meta:
        model = FCMDevice
        fields = ('id', 'user', 'device_id', 'registration_id', 'name', 'type')
        read_only_fields = ('user', 'name', 'type', 'device_id')

class RetrieveUpdateFavouriteRestaurantColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRestaurant
        fields = ('is_color',)