from rest_framework.views import APIView
from django.db.models.aggregates import Count
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .models import Collection, Product, Review, Customer
from .serializers import CollectionSerializers, ProductSerializers, ReviewSerializers, CustomerSerializers


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializers



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()  
    serializer_class = ProductSerializers


class ReviewViewSet(ModelViewSet):
    
    def get_queryset(self):
        return Review.objects.filter(seller_id=self.kwargs['customer_pk'])
    
    serializer_class = ReviewSerializers

    def get_serializer_context(self):
        return {'seller_id': self.kwargs['customer_pk']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related('user').all()
    serializer_class = CustomerSerializers