from channels.generic.websocket import AsyncJsonWebsocketConsumer
from chat.models import PublicChatRoom,PublicChatMessage
from channels.db import database_sync_to_async
from chat.exceptions import ClientError


class PublicChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print("Connected user:" + self.scope['user'])
        await self.accept()
        self.room_id=None

    async def disconnect(self):
        print("User disconnected!")
        try:
            if self.room_id!=None:
                await self.leave_room(self.room_id)
        except Exception:
            pass


    async def leave_room(self,room_id):
        is_auth=is_authenticated(self.scope['user'])
        room=await get_room_or_error(room_id)
        if is_auth:
            await self.disconnect_user(room_id,self.scope['user'])

        self.room_id=None
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )

        connected_users=get_connected_users(room_id)
        await self.channel_layer.group_send(
            room.group_name,
            {
                "type":"connected.user.count",
                "connected_user_count":connected_users
            }
        )

def get_connected_users(room):
    if room.users:
        return len(room.users.all())
    return 0


def is_authenticated(user):
    if user.is_authenticated:
        return True
    return False

@database_sync_to_async
def get_room_or_error(room_id):
    try:
        room=PublicChatRoom.objects.get(pk=room_id)
    except PublicChatRoom.DoesNotExist:
        raise ClientError("INVALID ROOM","room invalid!")
    return room

