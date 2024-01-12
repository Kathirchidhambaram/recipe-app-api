"""
    File to test user creation endpoint
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

CREATE_USER_URL = reverse('user:create')

def create_user(**payload):
    """
        Method to create user.
    """

    return get_user_model().objects.create(**payload)

class PublicUserApiTest(TestCase):

    def __init__(self):
        self.client = APIClient()

    def test_user_create_success(self):
        """
            Method to test whether user created successfully
        """

        payload = {
            'email' : 'Testuser@gmail.com',
            'password': 'Testpassword123',
            'name': 'Test User'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        # Testing whether create response is returned
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(
            email = payload['email']
        ) 

        # Testing whether password is correct
        self.assertTrue(user.check_password(payload['password']))

        # Testing password not in returned response
        self.assertTrue(payload['password'] not in res.data)

    def test_user_with_mail_exists(self):
        """
            Method to test whether given user already exists
        """
        payload = {
            'email' : 'Testuser@gmail.com',
            'password': 'Testpassword123',
            'name': 'Test User'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)