from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from crawler.models import Source
from teams.models import Team
from teams.serializers import TeamSerializer, UniverseSerializer


class TeamsCreateAPIView(CreateAPIView):
    request_serializer_class = UniverseSerializer
    response_serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        request_serializer = self.request_serializer_class(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        instance = Team.generate_random(request_serializer.data["universe"])
        response_serializer = self.response_serializer_class(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UniversesListAPIView(ListAPIView):
    serializer_class = UniverseSerializer

    def get_queryset(self):
        return Source.objects.all()
