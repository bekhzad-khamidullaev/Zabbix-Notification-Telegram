import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from .channels_ws.routing import websocket_urlpatterns
from .channels_ws.middleware import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JWTAuthMiddleware(URLRouter(websocket_urlpatterns)),
})
