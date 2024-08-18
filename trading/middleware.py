import jwt
from channels.middleware import BaseMiddleware
from django.conf import settings
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async


class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from django.contrib.auth.models import AnonymousUser
        from rest_framework_simplejwt.tokens import UntypedToken
        from django.contrib.auth import get_user_model

        User = get_user_model()
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")

        if token:
            try:

                # Decode the token to get the user information
                UntypedToken(token[0])
                decoded_data = jwt.decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
                user = await sync_to_async(User.objects.get)(id=decoded_data["user_id"])
                scope['user'] = user
            except jwt.ExpiredSignatureError:
                scope['user'] = AnonymousUser()
            except jwt.InvalidTokenError:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

