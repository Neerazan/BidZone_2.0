from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.db.models.deletion import ProtectedError
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import *
from .serializers import *

from .filters import ProductFilter, WishListItemFilter, AuctionFilter
from .pagination import DefaultPagination
from .permissions import *


class CollectionViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # pagination_class = DefaultPagination
    search_fields = ['title']
    ordering_fields = ['created_at', 'products_count']

    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]


    @action(detail=False, methods=['get'])
    def retrieve_by_title(self, request, title=None):
        try:
            collection = Collection.objects.annotate(products_count=Count('products')).get(title=title)
            serializer = self.serializer_class(collection)
            return Response(serializer.data)
        except Collection.DoesNotExist:
            return Response({"detail": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)
    

    @action(detail=False, methods=['get'])
    def retrieve_by_id(self, request, id=None):
        try:
            collection = Collection.objects.annotate(products_count=Count('products')).get(pk=id)
            serializer = self.serializer_class(collection)
            return Response(serializer.data)
        except Collection.DoesNotExist:
            return Response({"detail": "Collection not found."}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)







class CustomerCoinViewSet(ModelViewSet):
    #TODO: allow only GET Method
    # http_method_names = ['get', 'head', 'options']
    serializer_class = CustomerCoinSerializer

    def get_queryset(self):
        return UserCoin.objects.filter(customer_id=self.kwargs['customer_pk'])
    





class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsProductOwner]
    search_fields = ['title', 'description', 'collection__title']
    ordering_fields = ['price', 'updated_at']

    def get_queryset(self):
        return Product.objects.select_related('collection').prefetch_related('images').filter(customer_id=self.kwargs['customer_pk'])


    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response("Can not delete product because it is referenced by auction.", status=status.HTTP_400_BAD_REQUEST)
    

    def get_serializer_context(self):
        return {
            'customer_id': self.kwargs['customer_pk']
        }


    @action(detail=False, methods=['post'], url_path='bulk-delete', serializer_class=BulkDeleteSerializer)
    def bulk_delete(self, request, *args, **kwargs):

        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)

        product_ids = request.data.get('ids', [])
        if not product_ids:
            return Response({
                'detail': 'Product ids is required.'
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )


        products = Product.objects.filter(id__in=product_ids, customer_id=self.kwargs['customer_pk'])
        if not products:
            return Response({
                'detail': 'Products not found.'
            },
            status=status.HTTP_404_NOT_FOUND
        )


        try:
            deleted_count, _ =  products.delete()
            return Response({
                'detail': f'Successfully deleted {deleted_count} products.'
            },
            status=status.HTTP_204_NO_CONTENT
            )
        except ProtectedError:
            return Response({
                "detail":"Can not delete product because it is referenced by auction."
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    
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
        user_id = self.request.user.id
        reviewer = Customer.objects.get(user_id=user_id)
            

        return {
            'seller_id': self.kwargs['customer_pk'],
            'reviewer_id': reviewer.id
        }





class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['phone', 'membership', 'user__first_name', 'user__last_name']
    ordering_fields = ['user__first_name', 'user__last_name', 'created_at']
    filterset_fields = ['membership']


    def get_queryset(self):
        return Customer.objects.select_related('user').filter(user_id=self.request.user.id)


    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes = [IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.select_related('user').get(user_id=request.user.id)
        
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
    # pagination_class = DefaultPagination
    search_fields = ['id']
    ordering_fields = ['created_at']

    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer







class WishlistItemViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # pagination_class = DefaultPagination
    # search_fields = ['auction__product__title']
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
            .select_related('auction') \
            .prefetch_related('auction__product__images')

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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    serializer_class = AuctionSerializer

    search_fields = ['product__title', 'product__collection__title']
    ordering_fields = ['starting_time', 'current_price', 'bids_count']
    filterset_class = AuctionFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateAuctionSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = Auction.objects.select_related(
            'product', 'product__customer', 'product__customer__user'
        ).prefetch_related('product__images')
        queryset = queryset.annotate(bids_count=Count('bids'))
        return queryset


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'customer_id': self.request.user.id
        })
        return context

    @action(detail=True, methods=['get', 'put', 'delete'], permission_classes=[IsAuthenticated])
    def retrieve_by_slug(self, request, slug=None):
        try:
            auction = Auction.objects.annotate(bids_count=Count('bids')).get(product__slug=slug)
            if request.method == 'DELETE':
                # Check if bids to this auction exist or not if exist can not delete
                if auction.bids_count > 0:
                    return Response({"detail": "Can not delete auction because it has bids."}, status=status.HTTP_400_BAD_REQUEST)
                
                #If delete successful then change in_auction of product to false
                if auction.delete():
                    product = Product.objects.get(id=auction.product.id)
                    product.in_auction = False
                    product.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                
            elif request.method == 'PUT':
                # Handle update logic here
                
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED)  # Placeholder for PUT logic
            
            else:  # GET
                serializer = self.serializer_class(auction)
                return Response(serializer.data)
        except Auction.DoesNotExist:
            return Response({"detail": "Auction not found."}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['get', 'put', 'delete'], permission_classes=[IsAuthenticated])
    def retrieve_by_auction_id(self, request, auction_id=None):
        try:
            auction = Auction.objects.annotate(bids_count=Count('bids')).get(id=auction_id)
            if request.method == 'DELETE':
                # Check if bids to this auction exist or not if exist can not delete
                if auction.bids_count > 0:
                    return Response({"detail": "Can not delete auction because it has bids."}, status=status.HTTP_400_BAD_REQUEST)
                
                if auction.delete():
                    product = Product.objects.get(id=auction.product.id)
                    product.in_auction = False
                    product.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                
            elif request.method == 'PUT':
                auction_serializer = self.serializer_class(auction, data=request.data, partial=True)
                auction_serializer.is_valid(raise_exception=True)
                auction_serializer.save()
                return Response(auction_serializer.data)

            else:  # GET
                serializer = self.serializer_class(auction)
                return Response(serializer.data)
        except Auction.DoesNotExist:
            return Response({"detail": "Auction not found."}, status=status.HTTP_404_NOT_FOUND)



class AuctionChatViewSet(ModelViewSet):
    serializer_class = AuctionChatSerializer

    def get_queryset(self):
        return Chat.objects.filter(auction_id=self.kwargs['auction_pk'])

    def get_serializer_context(self):
        user_id = self.request.user.id
        customer = Customer.objects.get(user_id=user_id)
        return {
            'auction_id': self.kwargs['auction_pk'],
            'customer_id': customer.id
        }






class BidsViewSet(ModelViewSet):
    serializer_class = BidsSerializer
    filter_backends = [SearchFilter]
    search_fields =[ 'bidder__user__id' ]


    def get_queryset(self):
        return Bid.objects.select_related('bidder__user').filter(auction_id=self.kwargs['auction_pk']).order_by('-updated_at')
    

    def get_serializer_context(self):
        context =  super().get_serializer_context()
        auction_id = self.kwargs.get('auction_pk')
        
        if auction_id:
            context['auction_id'] = auction_id
        
        if self.request.user.is_authenticated:
            customer = Customer.objects.get(user_id=self.request.user.id)
            context['bidder_id'] = customer.id
            
        return context






class DeliveryViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = DeliverySerializer

    def get_queryset(self):
        return Delivery.objects.filter(customer_id=self.kwargs['customer_pk'])


class AuctionQuestionViewSet(ModelViewSet):
    serializer_class = AuctionQuestionSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        auction_id = self.kwargs['auction_pk']
        return Question.objects.filter(auction_id=auction_id).prefetch_related('answers').select_related('customer__user')


    def get_serializer_context(self):
        auction_id = self.kwargs['auction_pk']
        user_id = self.request.user.id
        return {
            'auction_id': auction_id,
            'customer_id': user_id
        }






class AuctionAnswerViewSet(ModelViewSet):
    serializer_class = AuctionAnswerSerializer

    def get_queryset(self):
        return Answer.objects.filter(question_id=self.kwargs['question_pk'])
    

    def get_serializer_context(self):
        question_id = self.kwargs['question_pk']
        user_id = self.request.user.id
        return {
            'question_id': question_id,
            'customer_id': user_id
        }






class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(customer_id=self.kwargs['customer_pk'])

    def get_serializer_context(self):
        return {
            'customer_id': self.kwargs['customer_pk']
        }



class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    http_method_names = ['get', 'head', 'options']
    
    def get_queryset(self):
        return Transaction.objects.filter(user_id=self.kwargs['customer_pk'])