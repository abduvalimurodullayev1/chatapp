from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.auth_views.login import LoginAPIView
from app.auth_views.logout import LogoutAPIView
from app.auth_views.register import RegisterApiView
from app.views import NewsLetterViewSet, MessageRetrieveAPIView, MessageListCreateAPIView, ProductViewSet, GroupMessageViewSet, GroupMessageCreateAPIView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),

    path('api/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('api/message/<int:pk>/', MessageRetrieveAPIView.as_view(), name='message-retrieve'),
    path('api/group/', GroupMessageCreateAPIView.as_view(), name='chat_group'),
    path('api/group/<int:pk>/', GroupMessageViewSet.as_view(), name='chat_group_detail'),

    path('news-letter/', NewsLetterViewSet.as_view(), name='news-letter'),

    path('', include(router.urls))
]
