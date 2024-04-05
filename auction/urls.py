from django.urls import path, include
from rest_framework import routers
from pprint import pprint
from .views import ProductViewSet, CollectionViewSet

router = routers.DefaultRouter()
router.register('product', ProductViewSet)
router.register('collection', CollectionViewSet)

urlpatterns = [
    path('', include(router.urls))
    # path('collection/', CollectionView.as_view()),
    # path('collection/<int:pk>/', CollectionDetailsView.as_view()),
    # path('products/', ProductList.as_view()),
    # path('products/<int:pk>', ProductDetails.as_view()),
]
