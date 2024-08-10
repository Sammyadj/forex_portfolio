from django.urls import path
from .consumers import PriceStreamConsumer

websocket_urlpatterns = [
    path('ws/stream/pricing/', PriceStreamConsumer.as_asgi()),
]