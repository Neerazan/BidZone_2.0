from datetime import timedelta

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import Auction, Bid, Delivery, Transaction, UserCoin


@shared_task
def process_completed_auctions():
    now = timezone.localtime().replace(second=0, microsecond=0)
    print(f'[DATE :::: TIME] {now}')

    # Use a small time range to account for any slight differences in ending_time
    time_range_start = now - timedelta(minutes=1)
    time_range_end = now + timedelta(minutes=1)

    completed_auctions = Auction.objects.filter(
        ending_time__range=(time_range_start, time_range_end), auction_status=Auction.AUCTION_ACTIVE
    )
    print(f'Completed auctions: {completed_auctions}')

    for auction in completed_auctions:
        with transaction.atomic():
            highest_bid = Bid.objects.filter(auction=auction, status=True).order_by('-amount').first()

            if highest_bid:
                auction.auction_status = Auction.AUCTION_COMPLETED
                auction.save()

                Delivery.objects.create(auction=auction, customer=highest_bid.bidder, status=Delivery.DELIVERY_STATUS_PENDING)

                other_bids = Bid.objects.filter(auction=auction, status=True).exclude(id=highest_bid.id)

                for bid in other_bids:
                    user_coin, created = UserCoin.objects.get_or_create(customer=bid.bidder)
                    user_coin.balance += bid.amount
                    user_coin.save()
                    bid.status = False
                    bid.save()

                    Transaction.objects.create(
                        invoice=f'Refunded for the auction {auction.product.title}',  # noqa: E251
                        user=bid.bidder,
                        amount=bid.amount,
                        transaction_type=Transaction.TRANSACTION_TYPE_REFUND,
                        transaction_status=Transaction.TRANSACTION_STATUS_COMPLETED,
                    )

                seller = auction.product.customer
                seller_coin, created = UserCoin.objects.get_or_create(customer=seller.id)
                seller_coin.balance += highest_bid.amount
                seller_coin.save()

                Transaction.objects.create(
                    invoice=f'Received {highest_bid.amount} for the auction {auction.product.title}',  # noqa: E251
                    user=seller,
                    amount=highest_bid.amount,
                    transaction_type=Transaction.TRANSACTION_TYPE_DEPOSITE,
                    transaction_status=Transaction.TRANSACTION_STATUS_COMPLETED,
                )
