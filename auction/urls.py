from django.urls import path, include
from .views import CollectionView

urlpatterns = [
    path('collection/', CollectionView.as_view(), name='collection-view')
]
