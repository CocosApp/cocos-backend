from .models import *
from rest_framework import serializers
from apps.restaurant.models import *
from apps.restaurant.serializers import *
from django.core.mail import send_mail

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id','name','photo')

class DiscountSerializer(serializers.ModelSerializer):

    card = CardSerializer(read_only=True)

    class Meta:
        model = Discount
        fields = ('id', 'name', 'card','porc','price','photo','promotion','terms_condition','descrip')

class DiscountAdminSerializer(serializers.ModelSerializer):

    restaurants = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Discount
        fields = ('id', 'name', 'card','porc','price','photo','terms_condition','finished_at','promotion','descrip','restaurants')

    def send_mail(self):
        send_mail('Un restaurante ha creado un nuevo descuento',
                  '''
                  Nombre del descuento: {}
                  Terminos y condicones:{}
                  Porcentaje: {}
                  Precio: {}
                  ¿Que promocion es? : {}
                  Fecha de vencimiento: {}
                  Para más información, observar aquí : http://backend.appcocos.com/admin/discount/discount/

                  '''.format(self.validated_data["name"], self.validated_data["terms_condition"],
                             self.validated_data["porc"], self.validated_data["price"],
                             self.validated_data["promotion"],self.validated_data["finished_at"]),
                  self.validated_data.get("email"), ['contacto@appcocos.com'], fail_silently=False)

class SubCategory1Serializer(serializers.ModelSerializer):  #I did this class because the other is genering conflicts

    class Meta:
        model = Subcategory
        fields = ('id','name','descrip','image')

class RestaurantBasic1Serializer(serializers.ModelSerializer): #I did this class because the other is genering conflicts

    subcategory = SubCategory1Serializer(many=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'subcategory', 'photo1')

class DiscountByCardSerializer(serializers.ModelSerializer):

    card = serializers.StringRelatedField()
    restaurants = RestaurantBasic1Serializer(many=True)

    class Meta:
        model = Discount
        fields = ('id','name','porc','descrip','card','restaurants')

class RestaurantByDiscountSerializer(serializers.ModelSerializer):

    discount = DiscountByCardSerializer(many=True,read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id','name', 'ruc','longitude','latitude','address','discount']