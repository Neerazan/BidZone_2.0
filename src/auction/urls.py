from django.urls import path
from rest_framework_nested import routers

from .views import *

# Your code here

router = routers.DefaultRouter()
router.register('collections', CollectionViewSet)
router.register('customers', CustomerViewSet, basename='customer')
router.register('wishlists', WishlistViewSet)
router.register('auctions', AuctionViewSet, basename='auction')

customer_router = routers.NestedDefaultRouter(router, 'customers', lookup='customer')
customer_router.register('reviews', ReviewViewSet, basename='customer-reviews')

customer_router.register('deliveries', DeliveryViewSet, basename='customer-deliveries')

customer_router.register('products', ProductViewSet, basename='customer-products')

customer_router.register('customer_coins', CustomerCoinViewSet, basename='customer-coins')

customer_router.register('addresses', AddressViewSet, basename='customer-addresses')

customer_router.register('transactions', TransactionViewSet, basename='customer-transactions')

products_router = routers.NestedDefaultRouter(customer_router, 'products', lookup='product')

products_router.register('images', ProductImageViewSet, basename='product-images')

wishlists_router = routers.NestedDefaultRouter(router, 'wishlists', lookup='wishlist')

wishlists_router.register('items', WishlistItemViewSet, basename='cart-items')

auction_router = routers.NestedDefaultRouter(router, 'auctions', lookup='auction')

auction_router.register('chats', AuctionChatViewSet, basename='auction-chats')

auction_router.register('bids', BidsViewSet, basename='auction-bids')

auction_router.register('questions', AuctionQuestionViewSet, basename='auction-questions')

answer_router = routers.NestedDefaultRouter(auction_router, 'questions', lookup='question')

answer_router.register('answers', AuctionAnswerViewSet, basename='question-answers')


# Collection Detail Path
def collection_detail_path(param_type, param_name, name_suffix):
    return path(
        f'collections/<{param_type}:{param_name}>/',
        CollectionViewSet.as_view(
            {
                'get': 'retrieve',
                'put': 'update',
                'delete': 'destroy',
            }
        ),
        name=f'collection-detail-{name_suffix}',
    )


urlpatterns = (
    [
        path(
            'auctions/<int:auction_id>/',
            AuctionViewSet.as_view(
                {
                    'get': 'retrieve_by_auction_id',
                    'put': 'retrieve_by_auction_id',
                    'delete': 'retrieve_by_auction_id',
                }
            ),
            name='auction_detail-id',
        ),
        path(
            'auctions/<slug:slug>/',
            AuctionViewSet.as_view({'get': 'retrieve_by_slug'}),
            name='auction-detail-slug',
        ),
        collection_detail_path('int', 'id', 'id'),
        collection_detail_path('slug', 'slug', 'slug'),
    ]
    + router.urls
    + customer_router.urls
    + wishlists_router.urls
    + auction_router.urls
    + products_router.urls
    + answer_router.urls
)
