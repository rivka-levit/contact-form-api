from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes
)

from message.serializers import MessageSerializer, MessageDetailSerializer

from core.models import Message
from core.permissions import AccessOwnerOnly


@extend_schema_view(
    list=extend_schema(
        description='List of all the messages that are not in ban.'
    ),
    create=extend_schema(description='Create a new message in the system.'),
    update=extend_schema(description='Full update of a message.'),
    partial_update=extend_schema(description='Partial update of a message.'),
    destroy=extend_schema(description='Remove a message from the system.'),
)
class MessageViewSet(ModelViewSet):
    """View for managing message APIs."""

    queryset = Message.objects.all()
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

    def get_queryset(self):
        """Filter and return queryset of messages."""

        queryset = super().get_queryset().filter(user=self.request.user)
        params = self.request.query_params.get('filter')
        if params:
            params = params.split(',')

            for param in params:
                if param == 'recent':
                    queryset = queryset.filter(is_recent=True)

        return queryset
