from django.conf.urls import url
from .views import *
from django.contrib.auth import views

urlpatterns = [
    url(r'^restaurant/list/$', RestaurantListAPIView.as_view()),
    url(r'^restaurantGPS/list/$',RestaurantGPSAPIView.as_view()),
    url(r'^restaurantBySubcategory/(?P<pk>\d+)/list/$', RestaurantBySubCategoryListAPIView.as_view()),
    url(r'^subcategory/list$', SubCategoryListAPIView.as_view()),
    url(r'^service/list$', ServiceListAPIView.as_view()),
    url(r'^schedule/list$', ScheduleListAPIView.as_view()),
    #Just admin
    url(r'^admin/create/restaurant$', CreateRestaurantAPIView.as_view()),
    url(r'^restaurant/RUD/(?P<pk>\d+)/$', RestaurantCRUDAPIView.as_view()),
    url(r'^admin/restaurant/RUD/(?P<pk>\d+)$', RestaurantCRUDAPIView.as_view()),
    url(r'^admin/restaurant/(?P<pk>\d+)/discount/listcreate$', ListRegisterRestaurantDiscountAPI.as_view()),
    url(r'^admin/restaurant/(?P<resdiscount>\w+)/discount$', RUDRestaurantDiscountAPI.as_view()),
    url(r'^admin/list/restaurantdiscount/$', ListRestaurantDiscountAPIView.as_view()),
]
