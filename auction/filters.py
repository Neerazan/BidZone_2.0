from django_filters.rest_framework import FilterSet
from .models import Product, WishlistItem

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'price': ['gt', 'lt']
        }


class WishListItemFilter(FilterSet):
    class Meta:
        model = WishlistItem
        fields = {
            'product__price': ['gt', 'lt']
        }