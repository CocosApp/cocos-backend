from django.core.urlresolvers import reverse, reverse_lazy
from django.conf.urls import url
from .views import *
from django.contrib.auth import views

urlpatterns = [
    url(r'^user/admin/register$', CreateUserAdminAPIView.as_view()),
    url(r'^user/admin/login$', LoginAdminAPIView.as_view(), name='login admin'),
    url(r'^user/admin/retrieve$', RetrieveUserAdminAPIView.as_view()),
    url(r'^user/admin/update$', UpdateUserAdminAPIView.as_view()),
    url(r'^user/admin/restaurant$', RetrieveUserAdminRestaurantAPIView.as_view()),
    url(r'^user/admin/restaurant/listcreate$', ListRegisterUserAdminRestaurantAPI.as_view()),
    url(r'^user/admin/restaurant/delete$', DestroyUserAdminRestaurantAPI.as_view()),
    url(r'^user/admin/(?P<adminrestaurant>\w+)/restaurant$', RUDUserAdminRestaurantAPI.as_view()),
    url(r'^change-password/$', ChangePasswordAPIView.as_view()),
    url(r'^register/$', CreateUserAPIView.as_view()),
    url(r'^login/$', LoginAPIView.as_view()),
    url(r'^webcontact/$', EmailWebContactAPIView.as_view()),
    url(r'^user/retrieve/$', RetrieveUserAPIView.as_view()),
    url(r'^login/mobile/(?P<backend>[^/]+)/$', FacebookMobileLoginAPI.as_view(), name="facebook-mobile-login"),
    url(r'^filter/users/$', FilterUsersAPIView.as_view()),
    url(r'^user/update/$', UpdateUserAPIView.as_view()),
    url(r'^user/(?P<pk>\d+)/photo/$', UpdateUserPhotoAPIView.as_view()),
    url(r'^user/recovery/(?P<id>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        {"post_reset_redirect": reverse_lazy(
            'account:password_reset_complete')},
        name='password_reset_confirm'),
    url(r'^user/reset/done/$', password_reset_complete, name='password_reset_complete'),
    url(r'^recovery/$', RecoveryPasswordAPI.as_view()),
    url(r'^user/favourite/restaurant/$', RetrieveFavRestaurantAPIView.as_view()),
    url(r'^favrestaurants/me/$', ListRegisterUserFavResAPI.as_view()),
    url(r'^user/(?P<userrestaurant>\w+)/restaurant$', RUDUserFavResAPI.as_view()),
    url(r'^user/favrestaurant/delete/me$', DestroyFavRestaurantAPI.as_view()),
    url(r'^me/devices/fcm/$', RegisterFCMDeviceAPI.as_view(), name='register-fcm-device'),
    url(r'^me/devices/fcm/update/$', UpdateFCMDeviceAPI.as_view(), name='update-fcm-device'),
    url(r'^favrestaurant/(?P<pk>\d+)/statuscolor$', RetrieveUpdateFavouriteRestaurantColorAPIView.as_view()),
]
