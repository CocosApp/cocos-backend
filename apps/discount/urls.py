from django.conf.urls import url
from .views import *
from django.contrib.auth import views

urlpatterns = [
    url(r'^discount/list/$', DiscountListAPIView.as_view()),
    url(r'^discount/create$', DiscountCreateAPIView.as_view()),
    url(r'^discount/CRUD/(?P<pk>\d+)/$', DiscountCRUDAPIView.as_view()),
    url(r'^discount/admin/CRUD/(?P<pk>\d+)$', DiscountAdminCRUDAPIView.as_view()),
    url(r'^card/list/$', CardListAPIView.as_view()),
    url(r'^admin/card/list$', CardListAdminAPIView.as_view()),
    url(r'^card/(?P<pk>\d+)/discount/restaurant$', DiscountByCardAPIView.as_view()),
    url(r'^discount/(?P<pk>\d+)/restaurant$', ListRestaurantsByCardAPIView.as_view()),

]
