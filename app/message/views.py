from django.db.models import Q

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

from datetime import datetime
import pytz


@extend_schema_view(
    list=extend_schema(
        description='List of all the messages that are not in ban.',
        parameters=[
            OpenApiParameter(
                'filter',
                OpenApiTypes.STR,
                required=False,
                description='Filter messages by one up to three parameters: '
                            '"recent", "read", "answered", separated by comma '
                            '(e.g. "recent,read" without quotes).'
            ),
            OpenApiParameter(
                'search',
                OpenApiTypes.STR,
                required=False,
                description='Filter messages by any string for searching it in'
                            ' the title, content and email fields of messages.'
            ),
            OpenApiParameter(
                'fd',
                OpenApiTypes.STR,
                required=False,
                description='Filter messages, starting from the indicated date '
                            'of creation (e.g. "2023-10-09" without quotes).'
            ),
            OpenApiParameter(
                'td',
                OpenApiTypes.STR,
                required=False,
                description='Filter messages up to the indicated date of '
                            'creation (e.g. "2023-10-09" without quotes).'
            ),
        ]
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
        filter_params = self.request.query_params.get('filter', None)
        search = self.request.query_params.get('search', None)
        fd = self.request.query_params.get('fd', None)
        td = self.request.query_params.get('td', None)

        if filter_params:
            filter_params = filter_params.split(',')
            qs_filtered = queryset.none()

            for param in filter_params:
                if param == 'recent':
                    qs_filtered = qs_filtered.union(queryset.filter(is_recent=True))
                if param == 'read':
                    qs_filtered = qs_filtered.union(queryset.filter(is_read=True))
                if param == 'answered':
                    qs_filtered = qs_filtered.union(queryset.filter(is_answered=True))

            queryset = qs_filtered

        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )

        if fd:
            y, m, d = map(int, fd.split('-'))
            from_date = datetime(y, m, d, 0, 0, 0, tzinfo=pytz.utc)

            queryset = queryset.filter(created_at__gte=from_date)

        if td:
            y, m, d = map(int, td.split('-'))
            to_date = datetime(y, m, d, 0, 0, 0, tzinfo=pytz.utc)

            queryset = queryset.filter(created_at__lt=to_date)

        return queryset
