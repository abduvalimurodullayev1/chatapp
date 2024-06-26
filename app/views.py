from django.db.models import Q
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from app.models import Message, NewsLetter, Product, GroupMessage
from app.permission import IsSenderOrReciever, IsMember
from app.serializer import MessageSerializer, MessageGetSerializer, NewsLetterSerializer, ProductSerializer, GroupMessageSerializer


class MessageListCreateAPIView(ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsSenderOrReciever]

    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class MessageRetrieveAPIView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageGetSerializer
    permission_classes = [IsAuthenticated, IsSenderOrReciever]


class NewsLetterViewSet(generics.ListCreateAPIView):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]


class GroupMessageViewSet(ListAPIView):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = [IsMember]
    lookup_field = 'pk'


class GroupMessageCreateAPIView(generics.CreateAPIView):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated]  # Update the permission classes if necessary

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
