from rest_framework import serializers
from decimal import Decimal
from .models import *

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
    images = ProductImageSerializer(many=True, read_only=True)

    def validate_product_delete(self, value):
        if Auction.objects.filter(pk=value).exists():
            raise serializers.ValidationError('This production is in auction, You can not delete it')
        return value

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'collection', 'price', 'images']
    

    def create(self, validated_data):
        customer_id = self.context.get('customer_id')
        return Product.objects.create(customer_id=customer_id, **validated_data)




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer_id', 'description']
    
    def create(self, validated_data):
        seller_id = self.context.get('seller_id')
        reviewer_id = self.context.get('reviewer_id')
        return Review.objects.create(seller_id=seller_id, reviewer_id=reviewer_id, **validated_data)




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




class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'product', 'current_price', 'ending_time', 'auction_status']




class AuctionChatSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        auction_id = self.context.get('auction_id')
        customer_id = self.context.get('customer_id')
        return Chat.objects.create(auction_id=auction_id, customer_id=customer_id, **validated_data)

    class Meta:
        model = Chat
        fields = ['id', 'auction_id', 'customer_id', 'message']





class DeliverySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Delivery
        fields = ['id', 'auction_id', 'customer_id', 'status', 'tracking_number', 'delivery_date']


class CustomerCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCoin
        fields = ['customer_id', 'balance']


class BidsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'auction_id', 'bidder_id', 'amount', 'status']
    

    def validate_amount(self, value):
        auction_id = self.context.get('auction_id')
        current_price = Auction.objects.get(id=auction_id).current_price
        bidder = self.context.get('bidder_id')
        balance = UserCoin.objects.get(customer=bidder).balance

        if value <= current_price:
            raise serializers.ValidationError("Bid Amount Must be grater than the current bid amount")

        if balance < value:
            raise serializers.ValidationError("You don't have enough balance to bid")
        
        return value


    def create(self, validated_data):
        auction_id = self.context.get('auction_id')
        bidder_id = self.context.get('bidder_id')

        auction = Auction.objects.get(pk=auction_id)
        auction.current_price = validated_data['amount']
        auction.save()

        customr_balance = UserCoin.objects.get(customer=bidder_id)
        customr_balance.balance = customr_balance.balance - validated_data['amount']
        customr_balance.save()

        return Bid.objects.create(bidder_id=bidder_id, auction_id=auction_id, **validated_data)