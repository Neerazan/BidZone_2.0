from django_filters.rest_framework import FilterSet
from .models import Product, WishlistItem, Auction

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
            'auction__product__price': ['gt', 'lt']
        }


class AuctionFilter(FilterSet):
    class Meta:
        model = Auction
        fields = {
            'product__collection': ['exact'],
            'current_price': ['gt', 'lt'],
        }