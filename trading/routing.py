from django.urls import path
from .consumers import PriceStreamConsumer, TradeConsumer, AccountInfoConsumer

websocket_urlpatterns = [
    path('ws/stream/pricing/', PriceStreamConsumer.as_asgi()),
    path('ws/api/trade/', TradeConsumer.as_asgi()),
    path("ws/account-info/", AccountInfoConsumer.as_asgi()),
]