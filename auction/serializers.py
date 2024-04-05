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

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.select_related('user').all())
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'collection', 'price', 'customer']

class ReviewSerializers(serializers.ModelSerializer):

    seller = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.select_related('user').all())
    reviewer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.select_related('user').all())
    class Meta:
        model = Review
        fields = ['id', 'seller', 'reviewer', 'description', 'created_at']


class CustomerSerializers(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'phone', 'membership', 'user']