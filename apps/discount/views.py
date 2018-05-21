from fcm_django.models import FCMDevice
from rest_framework import generics
from ..account.tasks import make_discounts_update
from apps.account.models import UserRestaurant
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from apps.discount.paginations import *


class CardListAPIView(generics.ListAPIView):
    pagination_class = TenPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer

    def get_queryset(self):
        make_discounts_update()
        return Card.objects.all()

class CardListAdminAPIView(generics.ListAPIView): #Just in front-end

    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated,)

class DiscountListAPIView(generics.ListAPIView):
    pagination_class = TenPagination
    permission_classes = (IsAuthenticated,)
    queryset = Discount.objects.filter(is_enable=True)
    serializer_class = DiscountSerializer


class DiscountCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DiscountAdminSerializer

    def perform_create(self, serializer):
        discount = serializer.save()
        restaurant = self.request.user.user_admrestaurants.first()
        print(restaurant.restaurant)
        print(restaurant)
        serializer.send_mail()
        make_discounts_update()
        if restaurant.restaurant:
            restaurant_discount = RestaurantDiscount.objects.create(discount=discount, restaurant=restaurant.restaurant)
            print(UserRestaurant.objects.filter(restaurant=restaurant.restaurant).count())
            for user_restaurant in UserRestaurant.objects.filter(restaurant=restaurant.restaurant):
                if FCMDevice.objects.filter(user=user_restaurant.user).exists():
                    fcm_devices = FCMDevice.objects.filter(user=user_restaurant.user)
                    print(restaurant.restaurant.name)
                    fcm_devices.send_message(
                        data = {
                        "title" :"Cocos",
                        "body" : "{0} tiene un nuevo descuento".format(restaurant.restaurant.name),
                        "restaurant_id": restaurant.restaurant.id,
                        "restaurant_name":restaurant.restaurant.name,
                    })

class DiscountCRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Discount.objects.filter(is_enable=True)
    serializer_class = DiscountSerializer

    def get_object(self):
        discount = Discount.objects.get(pk=self.kwargs['pk']).filter(is_enable=True)
        return discount

class DiscountAdminCRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Discount.objects.filter(is_enable=True)
    serializer_class = DiscountAdminSerializer

    def get_object(self):
        discount = Discount.objects.get(pk=self.kwargs['pk'])
        return discount

class DiscountByCardAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DiscountByCardSerializer

    def get_queryset(self):
        card = self.kwargs['pk']
        return Discount.objects.filter(card=card, is_enable=True)


class ListRestaurantsByCardAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantByDiscountSerializer

    def get_queryset(self):
        discount = self.kwargs['pk']
        return Restaurant.objects.filter(discount=discount, is_enable=True)
