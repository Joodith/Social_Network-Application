from channels.auth import channel_session_user_from_http
from learn_chat.models  import ChatRoom

@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({'accept':True})
    message.channel_session['rooms']=[]


def ws_disconnect(message):
    for room_id in message.channel_session.get('rooms',set()):
        try:
            room=ChatRoom.objects.get(id=room_id)
            room.websocket_group.discard(message.reply_channel)
        except ChatRoom.DoesNotExist:
            print("No room exists!")
