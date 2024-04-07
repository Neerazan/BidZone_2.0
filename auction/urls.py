from rest_framework_nested import routers
from .views import ProductViewSet, CollectionViewSet, ReviewViewSet, CustomerViewSet, WishlistViewSet, WishlistItemViewSet, ProductImageViewSet



router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)
# router.register('reviews', ReviewViewSet)
router.register('customers', CustomerViewSet)
router.register('wishlists', WishlistViewSet)
# router.register('product_image', ProductImageViewSet)

customer_router = routers.NestedDefaultRouter(router, 'customers', lookup='customer')
customer_router.register('reviews', ReviewViewSet, basename='customer-reviews')

wishlists_router = routers.NestedDefaultRouter(router, 'wishlists', lookup='wishlist')
wishlists_router.register('items', WishlistItemViewSet, basename='cart-items')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('images', ProductImageViewSet, basename='product-images')



urlpatterns = router.urls + customer_router.urls + wishlists_router.urls + products_router.urls


# urlpatterns = [
    # path('collection/', CollectionView.as_view()),
    # path('', include(customer_router.urls)),
    # path('collection/<int:pk>/', CollectionDetailsView.as_view()),
    # path('products/', ProductList.as_view()),
    # path('products/<int:pk>', ProductDetails.as_view()),
# ]
