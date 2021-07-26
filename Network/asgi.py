"""
ASGI config for Network project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application

from Network.websocket import websocket_application



os.environ['DJANGO_SETTINGS_MODULE']='Network.settings'
django.setup()



django_application=get_asgi_application()
async def application(scope,receive,send):
    if scope['type']=="http":
        await django_application(scope,receive,send)
    elif scope['type']=="websocket":
        await websocket_application(scope,receive,send)
    else:
        raise NotImplementedError(f"Unknown scope type:{scope['type']}")



    # Just HTTP for now. (We can add other protocols later.)

