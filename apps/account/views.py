from django.shortcuts import render
from rest_framework import generics, status, filters
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from social.apps.django_app.utils import psa
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.shortcuts import resolve_url, redirect
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from django.template.response import TemplateResponse
from .tasks import recovery_password_mail, send_invitation_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import deprecate_current_app
from django.contrib.auth import get_user_model
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

class EmailWebContactAPIView(generics.GenericAPIView):
    serializer_class = EmailWebContactSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.send_mail()
        return Response({'Correo envíado'}  ,status=status.HTTP_200_OK)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.get_user())
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class LoginAdminAPIView(generics.GenericAPIView):
    serializer_class = LoginAdminSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.get_user())
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class MobileLoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.get_user())
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class FacebookMobileLoginAPI(MobileLoginAPI):
    '''Facebook Login'''
    serializer_class = FacebookLoginSerializer

    @method_decorator(psa('account:facebook-mobile-login'))
    def dispatch(self, request, *args, **kwargs):
        return super(FacebookMobileLoginAPI, self).dispatch(request, *args, **kwargs)


class ChangePasswordAPIView(generics.GenericAPIView):
    '''Cambiar contraseña para usuario logueado'''
    permission_classes = IsAuthenticated,
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={"user": request.user})
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({"detail": "OK"}, status=status.HTTP_200_OK)


class RecoveryPasswordAPI(generics.GenericAPIView):
    '''Recuperar contraseña'''
    serializer_class = PasswordRecoverySerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        recovery_password_mail(vd.get("email"), request)
        return Response({"detail": "OK"}, status=status.HTTP_200_OK)


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class CreateUserAdminAPIView(generics.CreateAPIView):
    serializer_class = CreateUserAdminSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        serializer.send_mail()
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class RetrieveUserAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class RetrieveUserAdminAPIView(generics.RetrieveAPIView):
    serializer_class = RetrieveUserAdminSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        if self.request.user.is_admin_res == True:
            return self.request.user


class UpdateUserAPIView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UpdateUserPhotoAPIView(generics.UpdateAPIView):
    '''Actualizer fotos del usuario'''
    permission_classes = IsAuthenticated,
    serializer_class = UpdateUserPhotoSerializer

    def get_object(self):
        queryset = User.objects.get(pk=self.kwargs['pk'])
        return queryset


class FilterUsersAPIView(generics.ListAPIView):
    '''Filtrar usuarios por query params buscando por coincidencias en nombre o apellidos,ejemplo api/users/?search=erik'''
    queryset = User.objects.filter(is_superuser=False)
    pagination_class = PageNumberPagination
    serializer_class = UserFilterSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name')


@sensitive_post_parameters()
@never_cache
@deprecate_current_app
def password_reset_confirm(request, id=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert id is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        user = User.objects.get(pk=id)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@deprecate_current_app
def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


class RetrieveFavRestaurantAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListFavRestaurantSerializer

    def get_object(self):
        return self.request.user


class ListRegisterUserFavResAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUDUserRestaurantSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        return self.request.user.user_restaurants.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RetrieveUserRestaurantSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = RetrieveUserRestaurantSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        print(obj)
        if obj:
            serializer = RetrieveUserRestaurantSerializer(obj, context={'request': request})
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'detail': 'Usuario ya tiene este restaurante como favorito'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_create(self, serializer):
        user = self.request.user
        if not UserRestaurant.objects.filter(restaurant=serializer.validated_data.get('restaurant'),
                                             user=user).exists():
            serializer.save(user=user)
            print('*********************************')
            print(UserRestaurant.objects.filter(restaurant=serializer.validated_data.get('restaurant'),
                                             user=user))
            user_restaurant = UserRestaurant.objects.get(restaurant=serializer.validated_data.get('restaurant'),
                                             user=user)
            user_restaurant.is_color = True
            print(user_restaurant)
            print(user_restaurant.is_color)
            user_restaurant.save()
            return serializer
        else:

            print('=================================')
            return None


class RUDUserFavResAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUDUserRestaurantSerializer

    def get_object(self):
        id = self.kwargs.get('userrestaurant')
        return get_object_or_404(self.request.user.user_restaurants.all(), id=id)

    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        if object:
            serializer = RetrieveUserRestaurantSerializer(object, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'detail': 'El usuario asociado a este restaurante como favorito no existe'},
                            status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updt = self.perform_update(serializer)
        if updt:
            serializer = RetrieveUserRestaurantSerializer(updt, context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'detail': 'El Usuario ya esta amarrado a este restaurante como favorito'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_update(self, serializer):
        obj = serializer.validated_data
        obj_res = obj.get('restaurant')
        user = UserRestaurant.objects.filter(user=self.request.user)
        if obj_res:
            if not user.filter(restaurant=obj_res).exists():
                return serializer.save()
            else:
                return None
        else:
            return serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class RetrieveUserAdminRestaurantAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ListFavRestaurantSerializer

    def get_object(self):
        return self.request.user


class ListRegisterUserAdminRestaurantAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUDUserAdminRestaurantSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        return self.request.user.user_admrestaurants.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RetrieveUserAdminRestaurantSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = RetrieveUserAdminRestaurantSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        if obj:
            serializer = RetrieveUserAdminRestaurantSerializer(obj, context={'request': request})
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'detail': 'Admin ya tiene este restaurante '},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_create(self, serializer):
        user = self.request.user
        if not UserAdminRestaurant.objects.filter(restaurant=serializer.validated_data.get('restaurant'),
                                                  user=user).exists():
            user.save()
            return serializer.save(user=user)
        else:
            return None


class RUDUserAdminRestaurantAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUDUserAdminRestaurantSerializer

    def get_object(self):
        id = self.kwargs.get('adminrestaurant')
        return get_object_or_404(self.request.user.user_admrestaurants.all(), id=id)

    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        if object:
            serializer = RetrieveUserAdminRestaurantSerializer(object, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'detail': 'El admin asociado a este restaurante no existe'},
                            status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updt = self.perform_update(serializer)
        if updt:
            serializer = RetrieveUserAdminRestaurantSerializer(updt, context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'detail': 'El Admin ya esta amarrado a este restaurante'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_update(self, serializer):
        obj = serializer.validated_data
        obj_res = obj.get('restaurant')
        user = UserAdminRestaurant.objects.filter(user=self.request.user)
        if obj_res:
            if not user.filter(restaurant=obj_res).exists():
                return serializer.save()
            else:
                return None
        else:
            return serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class RegisterFCMDeviceAPI(generics.CreateAPIView):
    '''Registrar Dispositivo especificanco si es android o ios en el campo type'''
    serializer_class = FCMDeviceSerializer
    pagination_class = None
    permission_classes = IsAuthenticated,

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        device_id = serializer.validated_data.get("device_id")
        device = FCMDevice.objects.filter(device_id=device_id).first()
        if device:
            device.user = self.request.user
            device.name = vd.get("name")
            device.registration = vd.get("registration_id")
            device.save()
            return Response(FCMDeviceSerializer(device).data, status=status.HTTP_201_CREATED)
        else:
            serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateUserAdminAPIView(generics.UpdateAPIView):
    serializer_class = UpdateUserAdminSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UpdateFCMDeviceAPI(generics.UpdateAPIView):
    '''
        Enviar device_id y registration_id(token de android)
    '''
    permission_classes = IsAuthenticated,
    serializer_class = UpdateFCMDeviceSerializer

    def get_object(self):
        return get_object_or_404(FCMDevice.objects.filter(user=self.request.user),
                                 device_id=self.request.data.get('device_id'))


class DestroyFavRestaurantAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant.objects.all(), id=self.request.data.get('restaurant_id'))
        user_restaurant = get_object_or_404(self.request.user.user_restaurants.all(), restaurant=restaurant)
        user_restaurant.delete()
        return Response({'detail': 'Restaurante favorito eliminado'}, status=status.HTTP_204_NO_CONTENT)

class DestroyUserAdminRestaurantAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant.objects.all(), id=self.request.data.get('restaurant_id'))
        user_admrestaurant = get_object_or_404(self.request.user.user_admrestaurants.all(), restaurant=restaurant)
        user_admrestaurant.delete()
        return Response({'detail': 'Restaurante eliminado'}, status=status.HTTP_204_NO_CONTENT)

class RetrieveUpdateFavouriteRestaurantColorAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveUpdateFavouriteRestaurantColorSerializer

    def get_object(self):
        restaurant = Restaurant.objects.get(pk=self.kwargs['pk'])
        print(restaurant)
        user_restaurant = get_object_or_404(self.request.user.user_restaurants.all(), restaurant = restaurant)
        return user_restaurant

