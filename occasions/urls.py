from django.urls import path
from occasions.views import OccasionListView, OccasionDetailView

urlpatterns = [
    path('', OccasionListView.as_view()),
    path('<int:pk>/', OccasionDetailView.as_view()),
]