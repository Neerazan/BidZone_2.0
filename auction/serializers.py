from rest_framework import serializers
from decimal import Decimal
from .models import *
from django.db.models import Q

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


class SimpleCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name']



class BidsCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name']




class SimpleProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    customer = SimpleCustomerSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'customer', 'slug', 'description', 'price', 'images']




class WishlistProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ['title', 'description', 'slug', 'images']




class AuctionSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    bids_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Auction
        fields = ['id', 'product', 'current_price', 'bids_count', 'starting_time', 'ending_time', 'auction_status']





class WishlistAuctionSerializer(serializers.ModelSerializer):
    product = WishlistProductSerializer(read_only=True)
    bids_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Auction
        fields = ['id', 'product', 'current_price', 'bids_count', 'starting_time', 'ending_time', 'auction_status']




class WishlistItemSerializer(serializers.ModelSerializer):
    auction = WishlistAuctionSerializer(read_only=True)
    class Meta:
        model = WishlistItem
        fields = ['id', 'auction']





class WishlistSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    # items = WishlistItemSerializer(many=True, read_only=True)
    # total_price = serializers.SerializerMethodField()

    # def get_total_price(self, wishlist):
    #     return sum([item.product.price for item in wishlist.items.all()])
    class Meta:
        model = Wishlist
        # fields = ['id', 'items']
        fields = ['id']





class AddWishlistItemSerializer(serializers.ModelSerializer):
    auction = WishlistAuctionSerializer(read_only=True)
    auction_id = serializers.IntegerField(write_only=True)

    def validate_auction_id(self, value):
        if not Auction.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No Auction with this ID was found.')
        return value

    def save(self, **kwargs):
        wishlist_id = self.context['wishlist_id']
        auction_id = self.validated_data['auction_id']

        if WishlistItem.objects.filter(Q(wishlist_id=wishlist_id) & Q(auction_id=auction_id)).exists():
            raise serializers.ValidationError('This auction is already in the wishlist')
        
        wishlist_item = WishlistItem.objects.create(wishlist_id=wishlist_id, **self.validated_data)
        return wishlist_item

    class Meta:
        model = WishlistItem
        fields = ['auction_id', 'auction']  # Include auction_id in the fields

    def to_representation(self, instance):
        # Call the superclass's to_representation method to get the initial representation
        representation = super().to_representation(instance)
        
        # Use validated_data to access the auction_id safely
        auction_id = self.validated_data.get('auction_id')
        
        # Now that you have the auction_id, you can fetch the Auction instance
        if auction_id:
            auction = Auction.objects.get(pk=auction_id)
            # Serialize the Auction instance using the WishlistAuctionSerializer
            auction_serialized = WishlistAuctionSerializer(auction).data
            
            # Update the representation with the serialized Auction data
            representation['auction'] = auction_serialized
        else:
            # Handle the case where auction_id is not available
            # This could involve setting a default value or handling the absence of auction_id differently
            pass
        
        return representation







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


class AuctionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer', 'updated_at']

    def create(self, validated_data):
        try:
            question_id = self.context.get('question_id')
            customer_id = self.context.get('customer_id')
            return Answer.objects.create(question_id=question_id, customer_id=customer_id, **validated_data)
        except Exception as e:
            raise serializers.ValidationError('An error occurred while creating the answer')



class AuctionQuestionSerializer(serializers.ModelSerializer):
    answers = AuctionAnswerSerializer(many=True, read_only=True)
    customer = SimpleCustomerSerializer(read_only=True) 
    class Meta:
        model = Question
        fields = ['id', 'customer', 'question', 'answers', 'updated_at']
    

    def create(self, validated_data):
        try:
            auction_id = self.context.get('auction_id')
            customer_id = self.context.get('customer_id')
            return Question.objects.create(auction_id=auction_id, customer_id=customer_id, **validated_data)
        except Exception as e:
            raise serializers.ValidationError('An error occurred while creating the question', e)



class BidsSerializer(serializers.ModelSerializer):
    bidder = BidsCustomerSerializer(read_only=True)
    class Meta:
        model = Bid
        fields = ['id', 'auction_id', 'bidder', 'amount', 'status', 'created_at', 'updated_at']
    

    def validate_amount(self, value):
        auction_id = self.context.get('auction_id')
        current_price = Auction.objects.get(id=auction_id).current_price
        bidder_id = self.context.get('bidder_id')
        balance = UserCoin.objects.get(customer=bidder_id).balance


        if value <= current_price:
            raise serializers.ValidationError("Bid Amount Must be grater than the current bid amount")


        user_bid_exist = Bid.objects.filter(Q(auction_id=auction_id) & Q(bidder_id=bidder_id))
        if user_bid_exist.exists():
            existing_bid_amount = user_bid_exist.first().amount
            if balance < (value - existing_bid_amount):
                raise serializers.ValidationError("You don't have enough balance to bid")
            
        else:
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


    def update(self, instance, validated_data):
        auction = Auction.objects.get(pk=instance.auction_id)
        difference = validated_data['amount'] - instance.amount
        auction.current_price += difference
        auction.save()

        bidder_balance = UserCoin.objects.get(customer=instance.bidder_id)
        bidder_balance.balance += instance.amount - validated_data['amount']
        bidder_balance.save()

        return super().update(instance, validated_data)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['customer_id', 'province', 'district', 'municipality', 'ward', 'tole', 'street', 'zip_code']