
from rest_framework import viewsets, authentication, permissions
from recipe.serializers import RecipeSerializers, RecipeDetailSerializer
from core.models import Recipe

class RecipeViewset(viewsets.ModelViewSet):

    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all().order_by('-id')
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by('-id')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeSerializers
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Creating recipe"""

        serializer.save(user = self.request.user)