from django.contrib import admin
from django.http import HttpRequest
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline

from . import models


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title__istartswith', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:auction_product_changelist')
                + '?'
                + urlencode({
                    'collection__id': str(collection.id)
                }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'collection_title']
    list_select_related = ['collection'] #For optimization of query
    list_editable = ['price']
    autocomplete_fields = ['collection']
    list_per_page = 10
    search_fields = ['title__istartswith', 'price']
    list_filter = ['collection', 'updated_at']
    prepopulated_fields = {
        'slug': ['title']
    }
    exclude = ['promotion']
    
    def collection_title(self, product):
        return product.collection.title

    collection_title.short_description = 'Collection'

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'first_name',  'last_name', 'membership', 'birth_date', 'bids']
    list_editable = ['membership']
    list_select_related = ['user']
    # search_fields = ['first_name__istartswith', 'last_name__istartswith']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    list_filter = ['membership']
    ordering = ['user__first_name', 'user__last_name']
    
    @admin.display(ordering='bids_count')
    def bids(self,customer):
        url = (reverse('admin:auction_bid_changelist')
                + '?'
                + urlencode({
                    'bidder__id': str(customer.id)
                }))
        return format_html('<a href="{}">{}</a>', url, customer.bids_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            bids_count=Count('bid')
        )


@admin.register(models.Auction)
class AuctionAdmin(admin.ModelAdmin):
    #TODO: Queryset Optimization

    list_per_page = 10
    list_display = ['product', 'starting_price', 'current_price', 'starting_time', 'ending_time', 'auction_status', 'total_bids']
    list_editable = ['starting_price', 'current_price', 'auction_status']
    search_fields = ['product__title', 'auction_status', 'ending_time', 'starting_price', 'current_price']
    list_filter = ['auction_status']
    autocomplete_fields = ['product']

    def total_bids(self, auction):
        return auction.bid_set.count()
    
    total_bids.short_description = 'Bids'


@admin.register(models.Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['bidder', 'auction', 'amount', 'status']
    list_editable = ['status', 'amount']
    search_fields = ['amount', 'bidder__user__first_name', 'bidder__user__last_name', 'auction__product__title']
    autocomplete_fields = ['bidder', 'auction']


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'province', 'district', 'city', 'street']
    search_fields = ['province__istartswith', 'district__istartswith', 'city__istartswith', 'street__istartswith']
    list_filter = ['province']


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['auction', 'user', 'message']
    search_fields = ['message']
    autocomplete_fields = ['auction', 'user']



@admin.register(models.Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['auction', 'status', 'tracking_number', 'delivery_date', 'created_at']
    list_editable = ['status']
    search_fields= ['status', 'tracking_number', 'delivery_date', 'created_at']
    list_filter = ['status']
    autocomplete_fields =['user', 'auction']

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['seller', 'reviewer', 'description']
    search_fields = ['description']
    autocomplete_fields = ['seller', 'reviewer']


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']
    search_fields = ['product__title']


@admin.register(models.Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(models.WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['wishlist', 'product']