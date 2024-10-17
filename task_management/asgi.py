import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import task_management.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            task_management.routing.websocket_urlpatterns
        )
    ),
})