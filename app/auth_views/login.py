from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app.serializer import LoginModelSerializer


class LoginAPIView(APIView):

    @swagger_auto_schema(
        request_body=LoginModelSerializer,
        responses={
            status.HTTP_200_OK: "Login successfully",
            status.HTTP_400_BAD_REQUEST: "Invalid Credentials",
        }
    )
    def post(self, request):
        serializer = LoginModelSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['profile']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            # token, created = Token.objects.get_or_create(profile=profile)
            return Response(data={"Message": "Successfully login",
                                  # "token":token.key
                                  'access_token': access_token,
                                  'refresh_token': refresh_token},
                            status=status.HTTP_200_OK)
        return Response(data={"message": "Invalid Credentials"},
                        status=status.HTTP_400_BAD_REQUEST)
