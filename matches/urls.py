from django.urls import path
from matches.views import MatchesCreateAPIView


urlpatterns = [
    path("", MatchesCreateAPIView.as_view(), name="matches-create"),
]
