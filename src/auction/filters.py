from django_filters.rest_framework import FilterSet
from .models import Product, WishlistItem, Auction, Transaction

from django.db.models import Count
import django_filters



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


class AuctionFilter(django_filters.FilterSet):
    min_bids_count = django_filters.NumberFilter(method='filter_bids_count_min')
    max_bids_count = django_filters.NumberFilter(method='filter_bids_count_max')

    class Meta:
        model = Auction
        fields = {
            'product__collection': ['exact'],
            'current_price': ['gt', 'lt'],
            'auction_status': ['exact'],
            'product__customer__id': ['exact'],
        }

    def filter_bids_count_min(self, queryset, name, value):
        if value is not None:
            return queryset.annotate(bids_count=Count('bids')).filter(bids_count__gte=value)
        return queryset

    def filter_bids_count_max(self, queryset, name, value):
        if value is not None:
            return queryset.annotate(bids_count=Count('bids')).filter(bids_count__lte=value)
        return queryset


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'transaction_status': ['exact'],
            'transaction_type': ['exact'],
            'amount': ['gt', 'lt'],
            'created_at': ['gt', 'lt']
        }       
        