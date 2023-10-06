
"""
Serializers for message APIs.
"""

from rest_framework import serializers

from core.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for list of messages."""

    class Meta:
        model = Message
        fields = ['email', 'name', 'title']


class MessageDetailSerializer(MessageSerializer):
    """Serializer for single message."""

    class Meta(MessageSerializer.Meta):
        fields = [
            'email',
            'name',
            'title',
            'content',
            'is_recent',
            'is_read',
            'is_answered',
            'is_banned',
            'created_at'
        ]
        read_only_fields = ['created_at']
