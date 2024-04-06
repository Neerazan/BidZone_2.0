from rest_framework import serializers
from decimal import Decimal
from .models import Collection, Product, Review, Customer, Wishlist, WishlistItem
from core.serializers import UserSerializer

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.select_related('user').all())
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'collection', 'price', 'customer']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.select_related('user').all())
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'description']
    
    def create(self, validated_data):
        seller_id = self.context['seller_id']
        return Review.objects.create(seller_id=seller_id, **validated_data)


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'phone', 'membership', 'user']


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']

class WishlistItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = WishlistItem
        fields = ['id', 'product']


class WishlistSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = WishlistItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, wishlist):
        return sum([item.product.price for item in wishlist.items.all()])
    class Meta:
        model = Wishlist
        fields = ['id', 'items', 'total_price']
