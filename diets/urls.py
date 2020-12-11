from django.urls import path
from diets.views import DietListView, DietDetailView

urlpatterns = [
    path('', DietListView.as_view()),
    path('<int:pk>/', DietDetailView.as_view()),
]