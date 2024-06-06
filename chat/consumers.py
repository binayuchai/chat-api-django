import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom,Message
from .serializers import MessageSerializer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        message = text_data_json['message']
        user = self.scope['user']
        room = ChatRoom.objects.get(id=self.room_name)
        # Create message in the database
        msg = Message.objects.create(room=room, sender=user, content=message)
        
        # Serialize message
        serialized_msg = MessageSerializer(msg).data

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':serialized_msg
            }
        )
        
    
    async def chat_message(self,event):
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'message':message
        }))