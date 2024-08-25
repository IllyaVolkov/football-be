import uuid
import random

from django.core.validators import MinValueValidator
from django.db import models, transaction
from crawler.models import Source, Player

from utils.models import BaseModel


def calculate_score(value, low_value, high_value, low_score=1, high_score=100):
    """
    Calculates a score relatively to two edge values
    """
    if value <= low_value:
        return low_score
    elif value >= high_value:
        return high_score
    else:
        return low_score + (value - low_value) * (high_score - low_score) / (
            high_value - low_value
        )


class Team(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    size = models.IntegerField(default=5, validators=[MinValueValidator(1)])
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @staticmethod
    def generate_random(universe, team_size=5):
        try:
            source = Source.objects.get(name=universe)
        except Source.DoesNotExist:
            raise AttributeError(f"Source {universe} does not exist")

        players = Player.objects.filter(source=source)
        team_members = list(players.order_by("?")[:team_size])

        if len(team_members) < team_size:
            raise ValueError("Not enough players to generate team in chosen universe")

        with transaction.atomic():
            team = Team.objects.create(
                name=f"{team_members[0].name}'s team", size=team_size, source=source
            )
            team.assign_team_members(team_members)
        return team

    def assign_team_members(self, team_members):
        if len(team_members) < self.size:
            raise ValueError("Not enough players to fill the team")

        goalies_count = 1
        defence_count = random.randint(1, self.size - 2)

        goalies = sorted(team_members, key=lambda member: member.height, reverse=True)[
            :goalies_count
        ]
        for goaly in goalies:
            team_members.remove(goaly)
        defenders = sorted(
            team_members, key=lambda member: member.weight, reverse=True
        )[:defence_count]
        for defender in defenders:
            team_members.remove(defender)
        attackers = team_members

        team_members_bulk_create_list = []
        for player in goalies:
            team_members_bulk_create_list.append(
                TeamPlayer(
                    team=self,
                    player=player,
                    role=Role.GOALIE,
                    power=calculate_score(player.height, 100, 300),
                )
            )
        for player in defenders:
            team_members_bulk_create_list.append(
                TeamPlayer(
                    team=self,
                    player=player,
                    role=Role.DEFENCE,
                    power=calculate_score(player.weight, 20, 200),
                )
            )
        for player in attackers:
            team_members_bulk_create_list.append(
                TeamPlayer(
                    team=self,
                    player=player,
                    role=Role.OFFENCE,
                    power=calculate_score(
                        player.height, 30, 200, low_score=100, high_score=1
                    ),
                )
            )
        TeamPlayer.objects.bulk_create(team_members_bulk_create_list)


class Role(models.TextChoices):
    GOALIE = "G", "Goalie"
    DEFENCE = "D", "Defence"
    OFFENCE = "O", "Offence"


class TeamPlayer(BaseModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=Role.choices)
    power = models.FloatField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ("team", "player")
