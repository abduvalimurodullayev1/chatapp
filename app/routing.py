from django.urls import path
from app import consumers

websocket_urlpatterns = [
    path('ws/group/<int:group_id>/', consumers.GroupChatConsumer.as_asgi()),
]
