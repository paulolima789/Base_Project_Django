from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token", [None])[0]

        if token:
            user = await self.get_user(token)
            scope["user"] = user
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            access_token = AccessToken(token)
            return User.objects.get(id=access_token["user_id"])
        except Exception:
            return AnonymousUser()

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(inner)
