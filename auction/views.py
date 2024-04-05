from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models.aggregates import Count
from rest_framework import generics
from django.db.models import Prefetch


from .models import Collection, Product, Promotion
from .serializers import CollectionSerializers, ProductSerializers

class CollectionView(generics.ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializers

class CollectionDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializers

class ProductList(generics.ListCreateAPIView):
    #TODO: Optimize Query Problem

    queryset = Product.objects.all()
    serializer_class = ProductSerializers


    # def get(self, request):
    #     queryset = Product.objects.all()
    #     serializer = ProductSerializers(queryset, many=True)
    #     return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = ProductSerializers(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    # def get(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = ProductSerializers(product)
    #     return Response(serializer.data)
    
    # def put(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = ProductSerializers(product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    
    # def delete(self, request, pk):
    #     product = Product.objects.get(pk=pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)