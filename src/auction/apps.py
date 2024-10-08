from django.apps import AppConfig


class AuctionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.auction'

    def ready(self) -> None:
        import src.auction.signals  # noqa: F401
