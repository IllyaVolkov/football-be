from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from matches.models import Match
from matches.serializers import MatchCreateSerializer, MatchSerializer
from teams.models import Team


class MatchesCreateAPIView(CreateAPIView):
    request_serializer_class = MatchCreateSerializer
    response_serializer_class = MatchSerializer

    def create(self, request, *args, **kwargs):
        request_serializer = self.request_serializer_class(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        home_team = Team.objects.get(id=request_serializer.data["home_team"])
        visitor_team = Team.objects.get(id=request_serializer.data["visitor_team"])
        instance = Match.match(home_team, visitor_team)
        response_serializer = self.response_serializer_class(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
