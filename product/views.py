import generics
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
import django_filters.rest_framework
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend


class Pagin(PageNumberPagination):
    page_size = 2


from rest_framework import generics


# class RobotList(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     name = 'product-list'
#
#     filter_fields = (
#         'name',
#     )


@api_view(['GET', 'POST'])
# @authentication_classes([SessionAuthentication, JWTTokenUserAuthentication])
# @permission_classes([IsAuthenticated])
def all_product(request: Request):
    if request.method == 'GET':
        name = request.GET.get('name')
        if name is not None:
            products = Product.objects.filter(name__contains=name)
        else:
            products = Product.objects.all()
            product_serializer = ProductSerializer(products, many=True)
            return Response(product_serializer.data, status.HTTP_200_OK)
        if request.method == 'POST':
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(None, status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([SessionAuthentication, JWTTokenUserAuthentication])
# @permission_classes([IsAuthenticated])
def product_detail_view(request: Request, product_id: int):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response(None, status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data, status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(f'id ==> {serializer.data} edited', status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(f'id ==> {product_id} deleted', status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
# @authentication_classes([SessionAuthentication, JWTTokenUserAuthentication])
# @permission_classes([IsAuthenticated])
def create_category(request: Request):
    if request.method == 'GET':
        category = Category.objects.all()
        pagintor = Pagin()
        re = pagintor.paginate_queryset(category, request)
        ser_cat = CategorySerializer(re, many=True)
        return pagintor.get_paginated_response(ser_cat.data)
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)
