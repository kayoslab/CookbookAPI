from django.urls import path
from ingredients.views import IngredientListView, IngredientDetailView

urlpatterns = [
    path('', IngredientListView.as_view()),
    path('<int:pk>/', IngredientDetailView.as_view()),
]