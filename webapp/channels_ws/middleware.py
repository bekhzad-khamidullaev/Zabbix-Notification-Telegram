from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner
        self.auth = JWTAuthentication()

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        token = params.get('token')
        user = AnonymousUser()
        if token:
            token = token[0]
            try:
                validated = self.auth.get_validated_token(token)
                user = self.auth.get_user(validated)
            except Exception:
                pass
        scope['user'] = user
        return await self.inner(scope, receive, send)
