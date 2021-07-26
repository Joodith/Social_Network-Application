from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter,ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chat.consumers import PublicChatConsumer
from django.urls import path
from channels import route
import chat.routing
from django.conf.urls import url

application=ProtocolTypeRouter({
    'websocket':AllowedHostsOriginValidator(
 AuthMiddlewareStack(
URLRouter(
chat.routing.websocket_urlpatterns
 )
    )
    ),
})

def message_handler(message):
    print(message['text'])

channel_routing=[
    route("websocket.receive",message_handler)
]