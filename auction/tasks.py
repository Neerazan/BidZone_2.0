
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Auction, Bid, Delivery, UserCoin, Customer, Transaction
from django.db import transaction


@shared_task
def process_completed_auctions():
    now = timezone.localtime().replace(second=0, microsecond=0)
    print(f"[DATE :::: TIME] {now}")
    completed_auctions = Auction.objects.filter(ending_time=now, auction_status=Auction.AUCTION_ACTIVE)
    print(f"completed auctions: {completed_auctions}")

    with transaction.atomic():
        if completed_auctions:
            for auction in completed_auctions:
                heighest_bid = Bid.objects.filter(auction=auction).order_by('-amount').first()

                if heighest_bid:
                    auction.auction_status = auction.AUCTION_COMPLETED
                    auction.save()

                    delivery = Delivery.objects.create(
                        auction=auction,
                        user=heighest_bid.bidder,
                        status=Delivery.DELIVERY_STATUS_PENDING
                    )
                
                # Now return all the bids amount of other user, who have not won the auction
                # and refund their amount
                other_bids = Bid.objects.filter(auction=auction).exclude(id=heighest_bid.id)

                for bid in other_bids:
                    user_coin = UserCoin.objects.get(user=bid.bidder)
                    user_coin.amount += bid.amount
                    user_coin.save()
                    bid.status = False
                    bid.save()

                    #Save the Transaction
                    transaction = Transaction.objects.create(
                        invoice=f"Refunded for the auction {auction.product.title}",
                        user=bid.bidder,
                        amount=bid.amount,
                        transaction_type=Transaction.TRANSACTION_TYPE_REFUND,
                        transaction_status=Transaction.TRANSACTION_STATUS_COMPLETED
                    )

                    # Now deduct the amount from the winner and add the amount to the seller
                    seller = Customer.objects.get(user=auction.product.customer)
                    seller_coin = UserCoin.objects.get(user=seller.user)
                    seller_coin.amount += heighest_bid.amount
                    seller_coin.save()

                    #Save the Transaction
                    transaction = Transaction.objects.create(
                        invoice=f"Received {heighest_bid.amount} for the auction {auction.product.title}",
                        user=seller.user,
                        amount=heighest_bid.amount,
                        transaction_type=Transaction.TRANSACTION_TYPE_DEPOSIT,
                        transaction_status=Transaction.TRANSACTION_STATUS_COMPLETED
                    )


