from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.serializer import LogoutModelSerializer


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutModelSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'message': 'Siz muvaffaqiyatli tizimdan  chiqdingiz.'},
            status=status.HTTP_204_NO_CONTENT)
