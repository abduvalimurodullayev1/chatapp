from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated or request.method in ['GET']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.user


class IsSenderOrReciever(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow access only if the requesting user is the sender or receiver of the message.
        return obj.sender == request.user or obj.receiver == request.user


from rest_framework.permissions import BasePermission
from .models import ChatGroup, GroupMessage


class IsMember(BasePermission):
    message = 'Siz guruhga obuna bo\'lmagansiz ❌❌❌'

    def has_permission(self, request, view):
        # Assuming the object being accessed is a GroupMessage instance
        group_message = view.get_object()  # Retrieve the GroupMessage instance

        # Retrieve the associated ChatGroup for the GroupMessage
        chat_group = group_message.group  # Assuming 'group' is the ForeignKey to ChatGroup

        # Check if the requesting user is a member of the ChatGroup
        return chat_group.members.filter(id=request.user.id).exists()
