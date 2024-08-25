from rest_framework import serializers

from crawler.models import Source
from teams.models import Team, TeamPlayer, Role


class TeamPlayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="player.name", read_only=True)
    weight = serializers.FloatField(source="player.weight", read_only=True)
    height = serializers.FloatField(source="player.height", read_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = TeamPlayer
        fields = [
            "role",
            "power",
            "name",
            "weight",
            "height",
        ]

    def get_role(self, obj):
        return Role(obj.role).label


class TeamSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.name", read_only=True)
    players = TeamPlayerSerializer(source="teamplayer_set", many=True, read_only=True)
    power = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "source",
            "players",
            "power",
        ]

    def get_power(self, obj):
        return sum([p.power for p in obj.teamplayer_set.all()])


class UniverseSerializer(serializers.ModelSerializer):
    universe = serializers.CharField(source="name")

    class Meta:
        model = Source
        fields = ["universe"]

    def validate_universe(self, value):
        source_qs = Source.objects.filter(name=value)
        if not source_qs.exists():
            raise serializers.ValidationError(["This universe does not exist."])
        return value
