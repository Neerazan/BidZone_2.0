from django.contrib import admin
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4
from core.models import User

from .validators import validate_file_size


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=30)
    feaured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES =[
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()
    

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    @admin.display(ordering='user__email')
    def email(self):
        return self.user.email

    @admin.display(ordering='user__username')
    def username(self):
        return self.user.username

    class Meta:
        ordering = ['user__first_name']


class UserCoin(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='balance', primary_key=True)
    balance = models.PositiveIntegerField(default=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.customer.user.username} -> {self.balance}"
    
    class Meta:
        ordering = ['customer']


class Address(models.Model):
    province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255)
    ward = models.CharField(max_length=255)
    tole = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.customer.user.get_username()}'s Address"
    
    class Meta:
        ordering = ['province']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                validators=[MinValueValidator(Decimal(1))]
                                )
    
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotion = models.ManyToManyField(Promotion, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


class Auction(models.Model):
    AUCTION_ACTIVE = 'A'
    AUCTION_COMPLETED = 'C'
    AUCTION_CANCELLED = 'X'
    AUCTION_SCHEDULE = 'S'
    AUCTION_DELETED = 'D'

    AUCTION_STATUS_CHOICES = [
        (AUCTION_ACTIVE, "Active"),
        (AUCTION_COMPLETED, "Completed"),
        (AUCTION_CANCELLED, "Cancelled"),
        (AUCTION_SCHEDULE, "Schedule"),
        (AUCTION_DELETED, "Deleted"),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=starting_price)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    auction_status = models.CharField(max_length=1, choices=AUCTION_STATUS_CHOICES, default=AUCTION_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title}"
    
    class Meta:
        ordering = ['product']

class Bid(models.Model):
    bidder = models.ForeignKey(Customer, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False) #if true this is winning bid
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bidder.user.get_username()} bid {self.amount} for {self.auction.product.title}"
    
    class Meta:
        ordering = ['auction']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='auction/images', validators=[validate_file_size])

    def __str__(self):
        return self.product.title
    
    class Meta:
        ordering = ['product']


class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return f"{self.product.title}"



class Delivery(models.Model):
    DELIVERY_STATUS_PENDING = 'P'
    DELIVERY_STATUS_SHIPPED = 'S'
    DELIVERY_STATUS_OFD = 'O'
    DELIVERY_STATUS_FAILED = 'F'
    DELIVERY_STATUS_POSTPONE = 'D'

    DELIVERY_STATUS_COICES = [
        (DELIVERY_STATUS_PENDING, 'Pending'),
        (DELIVERY_STATUS_SHIPPED, 'Shipped'),
        (DELIVERY_STATUS_OFD, 'Out For Delivery'),
        (DELIVERY_STATUS_FAILED, 'Failed'),
        (DELIVERY_STATUS_POSTPONE, 'Postpone')
    ]

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = models.CharField(max_length=1, choices=DELIVERY_STATUS_COICES, default=DELIVERY_STATUS_PENDING)
    tracking_number = models.CharField(max_length=255, default="T001P")
    delivery_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for {self.auction} to {self.customer.user.get_username()}"
    
    class Meta:
        permissions = [
            ('cancel_delivery', 'Can cancel delivery')
        ]


class Review(models.Model):
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="received_reviews")
    reviewer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="written_reviews")
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer.user.get_username()} for {self.seller.user.get_username()}"


class Chat(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat on {self.auction.product.title} by {self.customer.user.get_username()}"


class Transaction(models.Model):
    TRANSACTION_TYPE_DEPOSITE = 'D'
    TRANSACTION_TYPE_BID = 'B'
    TRANSACTION_TYPE_REFUND = 'R'

    TRANSACTION_TYPE_CHOICES = [
        (TRANSACTION_TYPE_DEPOSITE, 'Deposite'),
        (TRANSACTION_TYPE_BID, 'Bid'),
        (TRANSACTION_TYPE_REFUND, 'Refund'),
    ]

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=1,choices=TRANSACTION_TYPE_CHOICES)
    reference_id = models.UUIDField(default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} by {self.user.user.get_username()}"
    


# Question and answer model for auction product
class Question(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question by {self.customer.user.get_username()} for {self.auction.product.title}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer by {self.customer.user.get_username()} for {self.question.auction.product.title}"