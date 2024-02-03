
from rest_framework import viewsets, authentication, permissions, mixins
from recipe.serializers import RecipeSerializers, RecipeDetailSerializer, TagSerializer
from core.models import Recipe, Tag

class RecipeViewset(viewsets.ModelViewSet):

    serializer_class = RecipeSerializers
    queryset = Recipe.objects.all().order_by('-id')
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tags = self.request.query_params.get('tags')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Creating recipe"""

        serializer.save(user = self.request.user)

class TagViewset(mixins.ListModelMixin, 
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by('-name')

    def patch(self):
        super().partial_update(self.request)