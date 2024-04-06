from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin

from .models import Collection, Product, Review, Customer, Wishlist, WishlistItem
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer, CustomerSerializer, WishlistSerializer, WishlistItemSerializer, AddWishlistItemSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description', 'collection__title']
    ordering_fields = ['price', 'updated_at']

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')

    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
        
    #     return queryset


class ReviewViewSet(ModelViewSet):
    
    def get_queryset(self):
        return Review.objects.filter(seller_id=self.kwargs['customer_pk'])
    
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'seller_id': self.kwargs['customer_pk']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related('user').all()
    serializer_class = CustomerSerializer


class WishlistViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet, DestroyModelMixin):

    queryset = Wishlist.objects.prefetch_related('items__product').all()
    serializer_class = WishlistSerializer


class WishlistItemViewSet(ModelViewSet):

    http_method_names = ['get', 'post', 'delete'] #it is case sensative
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddWishlistItemSerializer
        return WishlistItemSerializer

    def get_queryset(self):
        return WishlistItem.objects \
            .filter(wishlist_id=self.kwargs['wishlist_pk']) \
            .select_related('product')

    def get_serializer_context(self):
        return {'wishlist_id': self.kwargs['wishlist_pk']}