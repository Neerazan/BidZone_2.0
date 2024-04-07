from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.deletion import ProtectedError

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import *
from .serializers import *

from .filters import ProductFilter, WishListItemFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly


class CollectionViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['title']
    ordering_fields = ['created_at', 'products_count']

    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)




class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description', 'collection__title']
    ordering_fields = ['price', 'updated_at']

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response("Can not delete product because it is referenced by auction.", status=status.HTTP_400_BAD_REQUEST)

    #----------Custom Filter---------
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
        return {
            'seller_id': self.kwargs['customer_pk'],
            'reviewer_id': self.request.user.id
        }




class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.select_related('user').all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['phone', 'membership', 'user__first_name', 'user__last_name']
    ordering_fields = ['user__first_name', 'user__last_name', 'created_at']
    filterset_fields = ['membership']


    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes = [IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)




class WishlistViewSet(ModelViewSet):

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['id']
    ordering_fields = ['created_at']

    queryset = Wishlist.objects.prefetch_related('items__product').all()
    serializer_class = WishlistSerializer




class WishlistItemViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['product__title']
    ordering_fields = ['created_at']
    filterset_class = WishListItemFilter
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




class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {
            'product_id': self.kwargs['product_pk']
        }

class AuctionViewSet(ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer



class AuctionChatViewSet(ModelViewSet):
    serializer_class = AuctionChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(auction_id=self.kwargs['auction_pk'])

    def get_serializer_context(self):
        return {
            'auction_id': self.kwargs['auction_pk'],
            'user_id': self.request.user.id
        }