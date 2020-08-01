from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests the public users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test user is created with valid payload"""
        payload = {
            'email': 'test@yopmail.com',
            'password': 'password',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""
        payload = {
            'email': 'test@yopmail.com',
            'password': 'password',
            'name': 'Test User'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test password is more than 5 characters"""
        payload = {
            'email': 'test@yopmail.com',
            'password': 'pwd',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_valid_credentials(self):
        """Test the token is created with valid credentials"""
        payload = {
            'email': 'test@yopmail.com',
            'password': 'pwd'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """Test the token is not created with invalid credentials"""
        create_user(email='test@yopmail.com', password='pwd')

        invalid_pwd_payload = {
            'email': 'test@yopmail.com',
            'password': 'invalid'
        }
        res = self.client.post(TOKEN_URL, invalid_pwd_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

        invalid_email_payload = {
            'email': 'tests@yopmail.com',
            'password': 'pwd'
        }
        res = self.client.post(TOKEN_URL, invalid_email_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_fields(self):
        """Test email and password are required fields for token creation"""
        res = self.client.post(TOKEN_URL, {'email': '', 'password': ''})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
