from .models import *
from rest_framework import serializers
from apps.discount.serializers import *
from rest_framework.serializers import PrimaryKeyRelatedField

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = ('id','name','descrip','image')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name')


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'name')

class RestaurantSerializer(serializers.ModelSerializer):

    subcategory = SubCategorySerializer(read_only=True, many=True)
    service = ServiceSerializer(read_only=True, many=True)
    schedule = ScheduleSerializer(read_only=True,many=True)
    discount = DiscountSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = ('id','subcategory','name', 'ruc','longitude','latitude','address','whatsapp','facebook',
                  'schedule','discount','food_letter','mobile','photo1','photo2','photo3',
                  'service')

        read_only_fields = ('id',)

class RestaurantCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('id','name', 'ruc', 'longitude', 'latitude', 'address','food_letter','mobile','mobile2','whatsapp',
                  'facebook','photo1', 'photo2', 'photo3','subcategory','schedule','service','is_enable')
        read_only_fields = ('id',)

   #front end have to put "false" in is_enable

class RestauratGPSSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('id', 'name','address','longitude','latitude','location')

    def save(self, *args, **kwargs):
        self.location = 'POINT('+str(self.longitude) +' '+str(self.latitude)+')'
        return self.location

class RestaurantBasicSerializer(serializers.ModelSerializer):

    subcategory = SubCategorySerializer(many=True)
    user_restaurants = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model= Restaurant
        fields = ('id','name','subcategory','photo1','user_restaurants')


class CRUDRestaurantDiscountSerializer(serializers.ModelSerializer):
    discount = PrimaryKeyRelatedField(queryset=Discount.objects.all(), required=False)

    class Meta:
        model = RestaurantDiscount
        fields = ('discount',)

class RetrieveRestaurantDiscount1Serializer(serializers.ModelSerializer):

    discount = DiscountSerializer(read_only=True, required=False)

    class Meta:
        model = RestaurantDiscount
        fields = ('id', 'discount',)

class RetrieveRestaurantDiscountSerializer(serializers.ModelSerializer): #Object Iterable

    discount = DiscountSerializer(read_only=True, required=False,many=True)

    class Meta:
        model = RestaurantDiscount
        fields = ('id', 'discount',)

class RestaurantBasicSerializerAdmin(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ('id','name')


class DiscountSerializerAdmin(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = ('id','name')

class ListRestaurantDiscountSerializer(serializers.ModelSerializer):

    discount = DiscountSerializerAdmin(read_only=True, required=False)
    restaurant = RestaurantBasicSerializerAdmin(read_only=True, required=False)

    class Meta:
        model = RestaurantDiscount
        fields = ('id','restaurant','discount',)
