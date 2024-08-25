from rest_framework import serializers

from teams.models import Team
from matches.models import Match


class MatchCreateSerializer(serializers.Serializer):
    home_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    visitor_team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())

    def validate(self, attrs):
        home_team_id = attrs.get("home_team")
        visitor_team_id = attrs.get("visitor_team")

        if home_team_id == visitor_team_id:
            raise serializers.ValidationError(
                {"visitor_team": ["The team can't match against itself!"]}
            )
        return super().validate(attrs)


class MatchSerializer(serializers.ModelSerializer):
    home_team = serializers.CharField(source="home_team.name", read_only=True)
    visitor_team = serializers.CharField(source="visitor_team.name", read_only=True)
    winner = serializers.CharField(source="winner.name", read_only=True)

    class Meta:
        model = Match
        fields = [
            "home_team",
            "visitor_team",
            "winner",
            "highlights",
        ]
