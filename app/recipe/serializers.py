from rest_framework import serializers
from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag 
        fields = ['id', 'name']
        read_only = ['id']

class RecipeSerializers(serializers.ModelSerializer):

    tags = TagSerializer(many = True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only = ['id']

    def create(self, validated_data):

        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user

        print('tags', tags)
        for tag in tags:
            # Retrieving or Creating tag objects 
            tag_obj, created = Tag.objects.get_or_create(
                user = auth_user,
                **tag)
            recipe.tags.add(tag_obj)
        return recipe


class RecipeDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'time_minutes', 'price', 'link']
        read_only = ['id']

