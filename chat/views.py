from django.shortcuts import render
from useraccount.models import User
from rest_framework import generics,permissions
from chat.models import Message,ChatRoom

from chat.serializers import UserSerializer,MessageSerializer,ChatRoomSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class ChatRoomListView(generics.ListAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        room = ChatRoom.objects.get(id=room_id)
        return room.messages.all()
  

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        room_id = self.kwargs.get('room_id')
        room = ChatRoom.objects.get(id=room_id)
        serializer.save(sender=self.request.user, room=room)
