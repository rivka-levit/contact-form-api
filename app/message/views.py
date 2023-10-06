from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from message.serializers import MessageSerializer, MessageDetailSerializer

from core.models import Message
from core.permissions import AccessOwnerOnly


class MessageViewSet(ModelViewSet):
    """View for managing message APIs."""

    queryset = Message.objects.filter(is_banned=False)
    serializer_class = MessageDetailSerializer
    permission_classes = [IsAuthenticated, AccessOwnerOnly]

    def perform_create(self, serializer):
        """Create a new message and assign it to the user."""

        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return proper serializer to different actions."""

        if self.action == 'list':
            return MessageSerializer

        return self.serializer_class
