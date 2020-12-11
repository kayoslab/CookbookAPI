from django.urls import path
from cuisines.views import CuisineListView, CuisineDetailView

urlpatterns = [
    path('', CuisineListView.as_view()),
    path('<int:pk>/', CuisineDetailView.as_view()),
]