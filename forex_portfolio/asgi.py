import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from trading.routing import websocket_urlpatterns as trading_websocket_urlpatterns
from portfolio.routing import websocket_urlpatterns as portfolio_websocket_urlpatterns
from trading.middleware import JwtAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forex_portfolio.settings')

combined_websocket_urlpatterns = trading_websocket_urlpatterns + portfolio_websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JwtAuthMiddleware(
        AuthMiddlewareStack(
            URLRouter(
                combined_websocket_urlpatterns
            )
        )
    ),
})

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })

