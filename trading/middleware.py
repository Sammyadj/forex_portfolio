import jwt
from channels.middleware import BaseMiddleware
from django.conf import settings
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async


class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.models import AnonymousUser
        from rest_framework_simplejwt.tokens import UntypedToken, TokenError

        User = get_user_model()
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")

        if token:
            try:
                # Validate the token using UntypedToken (this checks the token's validity)
                UntypedToken(token[0])

                # Decode the token to extract the user information
                decoded_data = jwt.decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
                user = await sync_to_async(User.objects.get)(id=decoded_data["user_id"])
                scope['user'] = user

            except TokenError:
                # Token is invalid or expired
                scope['user'] = AnonymousUser()
            except jwt.ExpiredSignatureError:
                # Token has expired
                scope['user'] = AnonymousUser()
            except jwt.InvalidTokenError:
                # Token is invalid for any other reason
                scope['user'] = AnonymousUser()
            except User.DoesNotExist:
                # User does not exist in the database
                scope['user'] = AnonymousUser()
        else:
            # No token provided
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
