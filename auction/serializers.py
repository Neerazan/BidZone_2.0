from rest_framework import serializers
from decimal import Decimal
from .models import Collection, Product, Review, Customer
from core.serializers import UserSerializer

class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'collection', 'price', 'price_with_tax', 'seller']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax'
    )

    def calculate_tax(self, product: Product):
        return product.price * Decimal(1.1)


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'seller', 'reviewer', 'description', 'created_at']


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'phone', 'membership', 'user']
    user = UserSerializer()