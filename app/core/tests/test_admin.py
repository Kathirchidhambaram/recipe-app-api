"""
    Test file for testing admin page
"""

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

class AdminSiteTests(TestCase):

    def setUp(self):
        """
            Creating superuser and logging in
        """
        self.client = Client()

        # Creating and login for admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'testadmin@gmail.com',
            password = 'testpassword123'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email = 'testuser@gmail.com',
            password = 'testuser123'
        )
    
    def test_user_lists(self):
        """Test whether users are listed on client page"""


        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.email)