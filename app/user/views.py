# Create your views here.

from rest_framework import generics, authentication, permissions
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

class CreateUserView(generics.CreateAPIView):
    """Class based view for creating users"""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    
    serializer_class =  AuthTokenSerializer
    renderer_class = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """
        Class view to retrive and update user details
    """

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
