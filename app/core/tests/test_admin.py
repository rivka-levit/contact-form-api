"""
Tests for Django admin modifications.
"""

from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from rest_framework import status


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='test_admin_super@example.com',
            password='test_pass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test_admin_user@example.com',
            password='test_pass123',
            name='Sample Name'
        )

    def test_users_listed_success(self):
        """Test users are listed successfully."""

        url = reverse('admin:core_user_changelist')
        r = self.client.get(url)

        self.assertContains(r, self.user.email)
        self.assertContains(r, self.user.name)

    def test_user_edit_page_accessible(self):
        """Test edit user page works."""

        url = reverse('admin:core_user_change', args=[self.user.id])
        r = self.client.get(url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_user_create_page_works(self):
        """Test the create user page works."""

        url = reverse('admin:cor_user_add')
        r = self.client.get(url)

        self.assertEqual(r.status_code, status.HTTP_200_OK)
