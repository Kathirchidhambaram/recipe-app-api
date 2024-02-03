from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth import get_user_model
from django.urls import reverse
from core import models

from recipe.serializers import RecipeSerializers, RecipeDetailSerializer, TagSerializer

RECIPE_URLS = reverse('recipe:recipe-list')
TAG_URL = reverse('recipe:tag-list')

# Create your tests here.


def create_user(user = 'user@email.com', password = 'userpwd123'):
    """Helper function to create user
       @return :- Return the created user instance
    """

    return get_user_model().objects.create_user(email = user, password = password)

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
    recipe = models.Recipe.objects.create(**default)
    return recipe

def create_recipe_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_tag_url(tag_id):
    """Method to get tag detail url for given tag id"""
    return reverse('recipe:tag-detail', args=[tag_id])

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
        recipes = models.Recipe.objects.all().order_by('-id')

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
    
    def test_tag_model(self):
        """Testing the tag model and its string representation"""

        user = create_user()
        tag = models.Tag.objects.create(user = user, name = 'Tag1')

        self.assertEqual(str(tag), tag.name)

class PublicTagsApiTest(TestCase):
    """Tests for unauthenticated api requests"""

    def setUp(self):
        self.client = APIClient()
        
    def test_is_authenticated(self):
        
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTest(TestCase):
    """Tests for authenticated api requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_list_tags(self):
        """Test to check tag listings"""

        models.Tag.objects.create(user = self.user, name = "Dessert")
        models.Tag.objects.create(user = self.user, name = "Icecreams")

        res = self.client.get(TAG_URL)
        tags = models.Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_tag(self):
        """Test to patch tag details"""

        tag = models.Tag.objects.create(user = self.user, name = 'After Dinner')
        url = create_tag_url(tag.id)
        payload = {'name': 'Dessert'}
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Getting updated details in this model instance
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])
    
    def test_delete_tag(self):
        """Test to delete the existing tag"""

        tag = models.Tag.objects.create(user = self.user, name = 'Dinner')
        url = create_tag_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = models.Tag.objects.filter(user = self.user)
        self.assertFalse(tags.exists())

    def test_create_recipe_with_new_tags(self):
        """Test for creating recipes with new tags"""
        
        payload = {
        'title' : 'Thai sprawn',
        'time_minutes': 30,
        'price': 5.05,
        'tags': [{'name' : 'Thai'}, {'name' : 'Dinner'}]
            }
        
        res = self.client.post(RECIPE_URLS, payload, format = 'json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        created_recipes = models.Recipe.objects.filter(user = self.user)
        self.assertEqual(created_recipes.count(), 1)
        created_recipe = created_recipes[0]
        self.assertEqual(created_recipe.tags.count(), 2)

    def test_create_recipe_with_existing_tags(self):
        """Test for creating recipes with existing tags"""

        indian_tag = models.Tag.objects.create(user = self.user, name = 'Indian')

        payload = {
            'title' : 'Pongal',
            'time_minutes' : 40,
            'price' : 20,
            'tags' : [{'name' : 'Indian'}, {'name' : 'Breakfast'}]
        } 
        
        res = self.client.post(RECIPE_URLS, payload, format = 'json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        created_recipes  = models.Recipe.objects.filter(user = self.user)

        self.assertEqual(created_recipes.count(), 1)
        created_recipe = created_recipes[0]
        self.assertEqual(created_recipe.tags.count(), 2)

        self.assertIn(indian_tag, created_recipe.tags.all())