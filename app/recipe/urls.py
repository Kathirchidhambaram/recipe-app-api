from django.urls import path, include

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewset)
router.register('tag', views.TagViewset)
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]