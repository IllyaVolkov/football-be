from django.urls import path
from teams.views import TeamsCreateAPIView, UniversesListAPIView


urlpatterns = [
    path("", TeamsCreateAPIView.as_view(), name="teams-create"),
    path("universes", UniversesListAPIView.as_view(), name="universes-list"),
]
