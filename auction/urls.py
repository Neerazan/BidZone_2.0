from rest_framework_nested import routers
from .views import *


router = routers.DefaultRouter()
# router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)
router.register('customers', CustomerViewSet)
router.register('wishlists', WishlistViewSet)
router.register('auctions', AuctionViewSet)


customer_router = routers.NestedDefaultRouter(router, 'customers', lookup='customer')
customer_router.register('reviews', ReviewViewSet, basename='customer-reviews')
customer_router.register('deliveries', DeliveryViewSet, basename='customer-deliveries')
customer_router.register('products', ProductViewSet, basename='customer-products')


products_router = routers.NestedDefaultRouter(customer_router, 'products', lookup='product')
products_router.register('images', ProductImageViewSet, basename='product-images')


# products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
# products_router.register('images', ProductImageViewSet, basename='product-images')


wishlists_router = routers.NestedDefaultRouter(router, 'wishlists', lookup='wishlist')
wishlists_router.register('items', WishlistItemViewSet, basename='cart-items')


auction_router = routers.NestedDefaultRouter(router, 'auctions', lookup='auction')
auction_router.register('chats', AuctionChatViewSet, basename='auction-chats')
auction_router.register('bids', BidsViewSet, basename='auction-bids')


urlpatterns = router.urls + customer_router.urls + wishlists_router.urls + auction_router.urls + products_router.urls