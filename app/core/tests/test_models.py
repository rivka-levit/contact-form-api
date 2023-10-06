"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Message


def create_user(**params):
    """Create and return a new user."""

    defaults = {
        'email': 'user@example.com',
        'password': 'test_pass123'
    }
    defaults.update(**params)

    return get_user_model().objects.create_user(**defaults)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful."""

        email = 'test@example.com'
        password = 'test_pass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEquals(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email,
                password='sample123'
            )
            self.assertEquals(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without email raises ValueError"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', password='test123')

    def test_create_superuser(self):
        """Test creating a superuser"""

        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_message_success(self):
        """Test creating a message is successful."""

        user = create_user(email='test_message@example.com')
        data = {
            'name': 'Sample Name',
            'title': 'Sample title for message',
            'content': 'Full content of the message.'
        }
        msg = Message.objects.create(user=user, **data)

        self.assertTrue(Message.objects.filter(id=msg.id).exists())
        for attr, value in data.items():
            self.assertEqual(getattr(msg, attr), value)
        self.assertTrue(msg.is_recent)
        self.assertFalse(msg.is_read)
        self.assertFalse(msg.is_answered)
