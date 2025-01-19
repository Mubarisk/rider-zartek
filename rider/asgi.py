import django
from django.core.asgi import get_asgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rider.settings")
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa
# from channels.auth import AuthMiddlewareStack  # noqa
from ws.routing import websocket_urlpatterns  # noqa

application = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
