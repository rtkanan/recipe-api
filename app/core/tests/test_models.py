from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@yopmail.com"
        password = "Qwerty@123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the new user email is normalized"""
        email = 'test@YOPMAIL.COM'
        user = get_user_model().objects.create_user(
            email=email,
            password="Qwerty@123"
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "Qwerty@123")

    def test_create_super_user(self):
        """Test creating a new super user"""
        user = get_user_model().objects.create_superuser(
            email='test@yopmail.com',
            password="Qwerty@123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
