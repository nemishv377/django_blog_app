"""
ASGI config for django_blog_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application
# from chat import routing
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from chat.routing import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog_app.settings')
# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter(
#   {
#     "http": django_asgi_app,
#     "websocket": AllowedHostsOriginValidator(
#       AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
#     ),
#   }
# )



# import os

# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# application = ProtocolTypeRouter({
#   'http': get_asgi_application(),
# })





import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog_app.settings')

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  'websocket': AuthMiddlewareStack(
    URLRouter(
      routing.websocket_urlpatterns
    )
  ),
})


