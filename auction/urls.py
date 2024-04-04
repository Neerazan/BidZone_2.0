from django.urls import path, include
from .views import CollectionView, CollectionDetailsView

urlpatterns = [
    path('collection/', CollectionView.as_view()),
    path('collection/<int:pk>/', CollectionDetailsView.as_view())
]
