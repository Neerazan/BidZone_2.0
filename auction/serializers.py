from rest_framework import serializers
from decimal import Decimal
from .models import Collection, Product, Review, Customer, Wishlist, WishlistItem, ProductImage

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)



class ProductImageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id, **validated_data)
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image'] #product id is not defined here because it is already available in nested url


class ProductSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.select_related('user').all())
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'collection', 'price', 'customer', 'images']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.select_related('user').all())
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'description']
    
    def create(self, validated_data):
        seller_id = self.context['seller_id']
        return Review.objects.create(seller_id=seller_id, **validated_data)


class CustomerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'first_name', 'last_name', 'phone', 'birth_date', 'membership']


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
    items = WishlistItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, wishlist):
        return sum([item.product.price for item in wishlist.items.all()])
    class Meta:
        model = Wishlist
        fields = ['id', 'items', 'total_price']


class AddWishlistItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with this ID was found.')
        return value

    def save(self, **kwargs):
        wishlist_id = self.context['wishlist_id']
        return WishlistItem.objects.create(wishlist_id=wishlist_id, **self.validated_data)
    class Meta:
        model = WishlistItem
        fields = ['id', 'product_id']
