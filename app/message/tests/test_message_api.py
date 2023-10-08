"""
Tests for message APIs.
"""

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Message

MESSAGES_URL = reverse('message-list')


def detail_url(msg_id):
    """Create and return detail page url for a particular message."""

    return reverse('message-detail', args=[msg_id])


def create_user(**params):
    """Create and return a new user."""

    defaults = {
        'email': 'test@example.com',
        'password': 'test_pass_123'
    }
    defaults.update(**params)

    return get_user_model().objects.create_user(**defaults)


def create_msg(user, **params):
    """Create and return a message object."""

    defaults = {
        'email': 'subscriber@example.com',
        'name': 'John Doe',
        'title': 'Sample message title',
        'content': 'Sample content for the message'
    }
    defaults.update(**params)

    return Message.objects.create(user=user, **defaults)


class PublicMessageApiTests(TestCase):
    """Tests for requests from unauthorized users."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_list_unauthorized_error(self):
        """
        Test retrieving the list of messages fails for an unauthorized user.
        """

        r = self.client.get(MESSAGES_URL)

        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)


class PrivateMessageApiTests(TestCase):
    """Tests for authenticated user requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test_message@example.com')
        self.client.force_authenticate(self.user)

    def test_retrieve_list_msgs_success(self):
        """Test retrieve list of messages successfully."""

        create_msg(self.user)
        create_msg(self.user)

        r = self.client.get(MESSAGES_URL)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

    def test_create_message_success(self):
        """Test creating a new message successfully."""

        payload = {
            'email': 'msg_created@exapmle.com',
            'name': 'Me',
            'title': 'my super important question',
            'content': 'My very clear explanations.'
        }
        r = self.client.post(MESSAGES_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

        msg = Message.objects.get(id=r.data['id'])
        self.assertEqual(msg.user, self.user)

        for k, v in payload.items():
            self.assertEqual(r.data[k], v)

        auto_fields = (
            'is_recent',
            'is_read',
            'is_answered',
            'created_at'
        )
        for attr in auto_fields:
            self.assertIn(attr, r.data)

    def test_update_message_success(self):
        """Test updating a message successfully."""

        msg = create_msg(self.user)

        payload = {
            'is_recent': False,
            'is_read': True,
            'is_answered': True
        }
        r = self.client.patch(detail_url(msg.id), payload)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        msg.refresh_from_db()
        self.assertEqual(msg.is_recent, payload['is_recent'])
        self.assertEqual(msg.is_read, payload['is_read'])
        self.assertEqual(msg.is_answered, payload['is_answered'])

    def test_delete_message_success(self):
        """Test removing a message from the system."""

        msg = create_msg(self.user)
        r = self.client.delete(detail_url(msg.id))

        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_filtering_by_recent(self):
        """Test retrieving list of messages, filtering just recent."""

        create_msg(self.user)
        create_msg(self.user)
        create_msg(self.user, is_recent=False)

        params = {'filter': 'recent'}

        r = self.client.get(MESSAGES_URL, params)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)
