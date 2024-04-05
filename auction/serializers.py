from rest_framework import serializers
from decimal import Decimal
from .models import Collection, Product

class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'slug', 'collection', 'price', 'price_with_tax', 'seller']
    
    slug = serializers.SlugField(write_only=True)

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax'
    )

    def calculate_tax(self, product: Product):
        return product.price * Decimal(1.1)