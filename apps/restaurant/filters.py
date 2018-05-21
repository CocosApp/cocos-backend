import django_filters
from apps.restaurant.models import *

class RestaurantDiscountFilter(django_filters.FilterSet):

    restaurant = django_filters.CharFilter(name='restaurant__id')
    discount = django_filters.CharFilter(name='discount__id')

    class Meta:
        model = RestaurantDiscount
        fields = ('restaurant','discount')