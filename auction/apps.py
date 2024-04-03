from django.apps import AppConfig


class AuctionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auction'

    def ready(self) -> None:
        import auction.signals