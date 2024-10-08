from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from import_export.admin import ImportExportModelAdmin

from . import models
from .resources import ProductResource


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'products_count']
    search_fields = ['title__istartswith', 'products_count']

    # auto generated slug basead on title
    prepopulated_fields = {'slug': ['title']}

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:auction_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('products'))


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''

    class Media:
        css = {'all': ['auction/styles.css']}


@admin.register(models.Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['title', 'price', 'collection_title', 'in_auction']
    list_select_related = ['collection']  # For optimization of query
    list_editable = ['price']
    autocomplete_fields = ['collection']
    list_per_page = 10
    search_fields = ['title__istartswith', 'price']
    list_filter = ['collection', 'updated_at']
    # prepopulated_fields = {'slug': ['title']}
    readonly_fields = ['slug']
    exclude = ['promotion']

    def collection_title(self, product):
        return product.collection.title

    collection_title.short_description = 'Collection'

    resource_class = ProductResource


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'first_name', 'last_name', 'membership', 'birth_date', 'bids']
    list_editable = ['membership']
    list_select_related = ['user']
    # search_fields = ['first_name__istartswith', 'last_name__istartswith']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    list_filter = ['membership']
    ordering = ['user__first_name', 'user__last_name']

    @admin.display(ordering='bids_count')
    def bids(self, customer):
        url = reverse('admin:auction_bid_changelist') + '?' + urlencode({'bidder__id': str(customer.id)})
        return format_html('<a href="{}">{}</a>', url, customer.bids_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(bids_count=Count('bid'))


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = [
        'reference_id',
        'user',
        'invoice',
        'amount',
        'transaction_type',
        'transaction_status',
        'created_at',
    ]
    list_editable = ['transaction_status', 'transaction_type']


@admin.register(models.Auction)
class AuctionAdmin(admin.ModelAdmin):
    # TODO: Queryset Optimization

    list_per_page = 10
    list_display = [
        'product',
        'starting_price',
        'current_price',
        'starting_time',
        'ending_time',
        'auction_status',
        'total_bids',
    ]
    list_editable = ['starting_price', 'current_price', 'auction_status']
    search_fields = [
        'product__title',
        'auction_status',
        'ending_time',
        'starting_price',
        'current_price',
    ]
    list_filter = ['auction_status']
    autocomplete_fields = ['product']

    def total_bids(self, auction):
        return auction.bids.count()

    total_bids.short_description = 'Bids'


@admin.register(models.Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['bidder', 'auction', 'amount', 'status']
    list_editable = ['status', 'amount']
    search_fields = [
        'amount',
        'bidder__user__first_name',
        'bidder__user__last_name',
        'auction__product__title',
    ]
    autocomplete_fields = ['bidder', 'auction']


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'province',
        'district',
        'municipality',
        'ward',
        'tole',
        'zip_code',
        'street',
    ]
    search_fields = [
        'province__istartswith',
        'district__istartswith',
        'municipality__istartswith',
        'street__istartswith',
        'zip_code',
        'tole',
        'ward',
    ]
    list_filter = ['province']


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['auction', 'customer', 'message']
    search_fields = ['message']
    autocomplete_fields = ['auction', 'customer']


@admin.register(models.Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = [
        'auction',
        'customer_id',
        'status',
        'tracking_number',
        'delivery_date',
        'created_at',
    ]
    list_editable = ['status']
    search_fields = ['status', 'tracking_number', 'delivery_date', 'created_at']
    list_filter = ['status']
    autocomplete_fields = ['customer', 'auction']


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
    list_display = ['id', 'wishlist', 'auction']


@admin.register(models.UserCoin)
class UserCoinAdmin(admin.ModelAdmin):
    list_display = ['customer', 'balance']


@admin.register(models.Question)
class AuctionQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'auction', 'customer', 'question']
    # search_fields = ['question', 'answer']
    # autocomplete_fields = ['auction', 'customer']


@admin.register(models.Answer)
class AuctionAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_id', 'customer', 'answer']
