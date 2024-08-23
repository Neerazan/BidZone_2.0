from import_export import resources

from .models import Auction, Product


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


class AuctionResource(resources.ModelResource):
    class Meta:
        model = Auction
        # fields = ('id', 'product', 'start_date', 'end_date', 'starting_price', 'current_price', 'status', 'winner')
        # export_order = ('id', 'product', 'start_date', 'end_date', 'starting_price', 'current_price', 'status', 'winner')
