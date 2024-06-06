from django.urls import path
from chat.views import UserListView,MessageListView,SendMessageView,ChatRoomListView
from rest_framework.routers import DefaultRouter

app_name = "chat_app"

urlpatterns = [
    path('api/users/',UserListView.as_view(),name="user-list"),
    path('api/chatrooms/', ChatRoomListView.as_view(), name='chatroom-list'),

    path('api/chatrooms/<int:room_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('api/chatrooms/<int:room_id>/messages/send/', SendMessageView.as_view(), name='send-message'),
]
