"""
    Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.management import call_command

class ModelTests(TestCase):

    def test_user_created_by_email_successful(self):
        """
            Test to check whether user can be created via mail id sucessfully
        """

        email = 'test@gmail.com'
        password = 'testpassword123'
        
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        """
            Test to check whether user emails are normalized after creation
        """

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email = email, 
                                                        password = 'test123')
            self.assertEqual(user.email, expected_email)
    
    def test_create_super_user(self):

        user = get_user_model().objects.create_superuser('test@gmail.com', 'test1234')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    