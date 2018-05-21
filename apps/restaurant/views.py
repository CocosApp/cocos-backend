from rest_framework import generics,filters,status
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.restaurant.paginations import *
from rest_framework.filters import *
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from fcm_django.models import FCMDevice
from..account.tasks import *
from .filters import *


class SubCategoryListAPIView(generics.ListAPIView):
    pagination_class = TenPagination
    serializer_class = SubCategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    queryset = Subcategory.objects.all().order_by('priority')


class ServiceListAPIView(generics.ListAPIView):
    pagination_class = TenPagination
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

class ScheduleListAPIView(generics.ListAPIView):
    pagination_class = TenPagination
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

class RestaurantListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = TenPagination
    serializer_class = RestaurantBasicSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    queryset = Restaurant.objects.filter(is_enable=True).order_by('name')

class RestaurantGPSAPIView(generics.ListAPIView):

    serializer_class = RestaurantBasicSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        make_discounts_update()
        long = self.request.query_params.get('long',None)
        lat = self.request.query_params.get('lat', None)
        rad = self.request.query_params.get('rad',None)
        queryset = Restaurant.objects.filter(is_enable=True).order_by('name')

        if (long and lat and rad) is not None:
            pnt = GEOSGeometry('POINT('+str(long)+' '+str(lat)+')')
            queryset = Restaurant.objects.filter(is_enable=True,
                                                 location__distance_lte=(pnt, D(km=rad))).distance(pnt).order_by('distance')

        return queryset


class RestaurantBySubCategoryListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = TenPagination
    serializer_class = RestaurantBasicSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        subcategory=self.kwargs['pk']
        long = self.request.query_params.get('long', None)
        lat = self.request.query_params.get('lat', None)
        rad = self.request.query_params.get('rad', None)
        queryset = Restaurant.objects.filter(subcategory=subcategory, is_enable=True).order_by('name')

        if (long and lat and rad) is not None:
            pnt = GEOSGeometry('POINT(' + str(long) + ' ' + str(lat) + ')')
            queryset = queryset.filter(subcategory=subcategory,is_enable=True,
                                             location__distance_lte=(pnt, D(km=rad))).distance(pnt).order_by('distance')

        return queryset


#Now, we have to work with the admin restaurants

class CreateRestaurantAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RestaurantCreateSerializer


class RestaurantCRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_object(self):
        make_discounts_update()
        res = Restaurant.objects.get(pk=self.kwargs['pk'])
        return res

class ListRegisterRestaurantDiscountAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUDRestaurantDiscountSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        restaurant = self.kwargs['pk']
        return Restaurant.objects.filter(id=restaurant)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RetrieveRestaurantDiscountSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = RetrieveRestaurantDiscountSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        if obj:
            serializer = RetrieveRestaurantDiscount1Serializer(obj, context={'request': request})
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'detail': 'El restaurante ya tiene este descuento '},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_create(self, serializer):
        id = self.kwargs['pk']
        restaurant = Restaurant.objects.get(id=id)

        if not RestaurantDiscount.objects.filter(discount=serializer.validated_data.get('discount'),
                                           restaurant=restaurant).exists():
            restaurant.save()
            return serializer.save(restaurant=restaurant)
        else:
            return None

class RUDRestaurantDiscountAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CRUDRestaurantDiscountSerializer

    def get_object(self):
        id = self.kwargs.get('resdiscount')
        return get_object_or_404(RestaurantDiscount.objects.all(), id=id)

    def retrieve(self, request, *args, **kwargs):
        object = self.get_object()
        if object:
            serializer = RetrieveRestaurantDiscount1Serializer(object, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'detail': 'El restaurante asociado a este descuento no existe'},
                            status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updt = self.perform_update(serializer)
        if updt:
            serializer = RetrieveRestaurantDiscount1Serializer(updt, context={'request': request})
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'detail': 'El restaurante ya esta amarrado a este descuento'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_update(self, serializer):
        obj = serializer.validated_data
        obj_dis = obj.get('discount')
        restaurant = RestaurantDiscount.objects.filter(is_enable=True)
        if obj_dis:
            if not restaurant.filter(discount=obj_dis).exists():
                return serializer.save()
            else:
                return None
        else:
            return serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class ListRestaurantDiscountAPIView(generics.ListAPIView):

    serializer_class = ListRestaurantDiscountSerializer
    queryset = RestaurantDiscount.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = RestaurantDiscountFilter


