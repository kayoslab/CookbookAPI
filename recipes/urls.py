from django.urls import path
from recipes.views import RecipeListView, RecipeDetailView

urlpatterns = [
    path('', RecipeListView.as_view()),
    path('<int:pk>/', RecipeDetailView.as_view()),
]