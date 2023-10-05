"""
Tests for user APIs.
"""

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
# PROFILE_URL = reverse('user:profile')


def create_user(**params):
    """Create and return a new user."""

    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests for requests from unauthorized users."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""

        payload = {
            'email': 'test@example.com',
            'password': 'test_pass12345'
        }
        r = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertTrue(exists)

    def test_create_user_empty_email_fails(self):
        """Test creating a user without email fails."""

        payload = {'email': '', 'password': 'test_pass12345'}
        r = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_email_exists_fails(self):
        """Test creating a user fails if the email already exists in db."""

        create_user(email='test@example.com', password='test_pass_123')

        payload = {
            'email': 'test@example.com',
            'password': 'test_pass12345'
        }
        r = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_small_password_fails(self):
        """Test creating a user with password less than 8 characters fails."""

        payload = {
            'email': 'test_pass@example.com',
            'password': 't_p12'
        }
        r = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""

        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123'
        }
        create_user(**user_details)
        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        r = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', r.data)
        self.assertEquals(r.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""

        create_user(email='test@example.com', password='good_pass')
        payload = {'email': 'test@example.com', 'password': 'bad_pass'}

        r = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', r.data)
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""

        payload = {'email': 'test@example.com', 'password': ''}

        r = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', r.data)
        self.assertEquals(r.status_code, status.HTTP_400_BAD_REQUEST)
