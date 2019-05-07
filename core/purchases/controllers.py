#rest_framework
from rest_framework.response import *
from rest_framework import status, views, viewsets, pagination, filters
from rest_framework import *
from datetime import datetime

#django
from django.contrib.contenttypes.models import *
from django.http import *

#3rd party
from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection

#local
from .serializers import *
from core.serializers import *
from core.models import *
from core.utils import *

class PurchaseController(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    pagination_class = PagePagination
    queryset = Item.objects.all().filter(isDelete=False)
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend]
    search_fields = ['purchaseId','itemId__itemName','purchaseDescription']
    filter_fields = ['createdDate',]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.is_valid(raise_exception=True)
            # self.perform_create(serializer)
            purchaseQuantity = serializer.data['purchaseQuantity']
            purchaseDescription = serializer.data['purchaseDescription']
            itemId = None
            if serializer.data['itemId']:
                itemId = Item.objects.get(itemId=serializer.data['itemId'])
            
            purchases = Purchase.objects.create(
                purchaseQuantity = purchaseQuantity,
                purchaseDescription = purchaseDescription,
                itemId = itemId
            )
            purchases.save()

            # Overriding when create a purchase instance, quantity of items is also added
            if itemId and purchaseQuantity:
                items = Item.objects.get(itemId=purchases.itemId.itemId)
                items.itemQuantity = items.itemQuantity+purchaseQuantity
                items.save()

            headers = self.get_success_headers(serializer.data)
            serializer = RespPurchaseSerializer(purchases)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        qry = self.filter_queryset(Purchase.objects.all().filter(isDelete=False))

        page = self.paginate_queryset(qry)
        if page:
            serializer = RespPurchaseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = RespPurchaseSerializer(qry, many=True)
        return Response({'result': serializer.data})

    def retrieve(self, request, pk, *args, **kwargs):
        instance = Purchase.objects.filter(purchaseId=pk, isDelete=False)

        try:
            obj = instance.get()
        except:
            raise Http404()
        
        serializer = RespPurchaseSerializer(obj)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # if serializer.is_valid():
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = RespPurchaseSerializer(data=request.data)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            serializer = RespPurchaseSerializer(data=request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Overriding DELETE method from hard delete to soft delete
    def perform_destroy(self, instance):
        instance.isDelete=True
        instance.save()