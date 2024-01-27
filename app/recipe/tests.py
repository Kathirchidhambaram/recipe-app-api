from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Recipe

from recipe.serializers import RecipeSerializers, RecipeDetailSerializer

RECIPE_URLS = reverse('recipe:recipe-list')
# Create your tests here.


# Helper function to create Recipe models
def create_recipe(user, **params):
    default = {
        'user' : user,
        'title' : 'Test title',
        'description' : 'Test description',
        'time_minutes': 5,
        'price': 5.05,
        'link': 'http://testrecipe.pdf'
    }

    default.update(params)

    # Creating recipe
    recipe = Recipe.objects.create(**default)
    return recipe

def create_recipe_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])

class PublicAPITest(TestCase):
    """Test for unauthenticated users"""

    def setUP(self):
        self.client = APIClient()
    
    def test_list_recipes(self):
        """Test to list recipes"""
        res = self.client.get(RECIPE_URLS)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
class PrivateAPITest(TestCase):
    """Test for authenticated users"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email = 'testuser@email.com',
            password = 'testpwd1234'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test to retrieve list of recipes"""

        create_recipe(user = self.user)
        create_recipe(user = self.user)

        res = self.client.get(RECIPE_URLS)
        recipes = Recipe.objects.all().order_by('-id')

        serializer = RecipeSerializers(recipes, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_recipe_details(self):
        """Test for recipe details of single recipe"""

        recipe = create_recipe(user=self.user)

        url = create_recipe_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)