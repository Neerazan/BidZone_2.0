
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Auction, Bid, Delivery


@shared_task
def process_completed_auctions():
    now = timezone.localtime().replace(second=0, microsecond=0)
    print(f"[DATE :::: TIME] {now}")
    completed_auctions = Auction.objects.filter(ending_time=now)
    print(f"Time completed: {completed_auctions}")

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