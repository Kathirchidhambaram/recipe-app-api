"""
    File to test user creation endpoint
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(payload):
    """
        Method to create user.
    """

    return get_user_model().objects.create_user(email = payload['email'], 
                                           password = payload['password'],
                                           name = payload['name'])

class PublicUserApiTest(TestCase):

    def setUp(self):
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
        create_user(payload)

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
    
    def test_create_token_user(self):
        """
            Test creating token for user after posting credentials
        """

        payload = {
            'email':'testuser@gmail.com',
            'password': 'testpwd123',
            'name': 'Test User'
        }

        create_user(payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_bad_credentials(self):
        """
            Test to check whether bad credentials are receiving token
        """

        payload = {
            'email':'testuser@gmail.com',
            'password': 'testpwd123',
            'name': 'Test User'
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token',  res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_access_me(self):
        """
            Test to check whether user access me page without authentication
        """
        payload = {
            'email':'testuser@gmail.com',
            'password': 'testpwd123',
            'name': 'Test User'
        }
        res = self.client.get(ME_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        payload =  {'email':'test@example.com',
            'password':'testpass123',
            'name' :'Test Name'}
        self.user = create_user(payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)