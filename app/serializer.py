from tokenize import TokenError

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from app.models import Message, NewsLetter, Product, User, ChatGroup, GroupMessage
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'image']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ()


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ()


class MessageGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ()


class NewsLetterSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username', read_only=True)
    user_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NewsLetter
        fields = ['id', 'user', 'user_username', 'user_image', 'comment', 'created_at']

    def get_user_image(self, instance):
        user = instance.user
        if user and hasattr(user, 'image') and user.image:
            return user.image.url
        return None

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user and not request.user.is_anonymous:
            validated_data['user'] = request.user
        return super(NewsLetterSerializer, self).create(validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'image']
        extra_kwargs = {
            'phone_number': {'read_only': True}
        }


class LoginModelSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        if phone_number and password:
            user = authenticate(username=phone_number, password=password)
            if not user:
                raise serializers.ValidationError("Incorrect credentials")
        else:
            raise serializers.ValidationError("Both phone number and password are required")

        data['profile'] = user
        return data


class LogoutModelSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh_token']
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError(
                "Token eskirgan yoki not'g'ri"
            )


class RegisterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        hashed_password = make_password(password)
        user = User.objects.create(**validated_data,
                                   password=hashed_password)
        return user


class GroupMessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=ChatGroup.objects.all())

    class Meta:
        model = GroupMessage
        fields = ['id', 'group', 'sender', 'content', 'date']
