from django.urls import path, include
from .views import CollectionView, CollectionDetailsView, ProductList, ProductDetails

urlpatterns = [
    path('collection/', CollectionView.as_view()),
    path('collection/<int:pk>/', CollectionDetailsView.as_view()),
    path('products/', ProductList.as_view()),
    path('products/<int:pk>', ProductDetails.as_view()),
]
