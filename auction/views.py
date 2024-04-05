from django.db.models.aggregates import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .filters import ProductFilter
from .models import Collection, Product, Review, Customer
from .serializers import CollectionSerializers, ProductSerializers, ReviewSerializers, CustomerSerializers


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializers



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'collection__title']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')

    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
        
    #     return queryset


class ReviewViewSet(ModelViewSet):
    
    def get_queryset(self):
        return Review.objects.filter(seller_id=self.kwargs['customer_pk'])
    
    serializer_class = ReviewSerializers

    def get_serializer_context(self):
        return {'seller_id': self.kwargs['customer_pk']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related('user').all()
    serializer_class = CustomerSerializers