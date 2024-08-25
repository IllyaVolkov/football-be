import random
from django.db import models

from teams.models import Team, TeamPlayer, Role
from utils.models import BaseModel


class Match(BaseModel):
    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home_matches"
    )
    visitor_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="visitor_matches"
    )
    winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_matches",
    )
    highlights = models.JSONField(default=list)

    def __str__(self):
        return f"{self.home_team} vs {self.visitor_team}"

    @staticmethod
    def match(home_team, visitor_team, duration=90):
        home_score, visitor_score = 0, 0
        highlights = []

        home_team_players = list(
            TeamPlayer.objects.filter(team=home_team).annotate(
                name=models.F("player__name")
            )
        )
        for player in home_team_players:
            player.power += 1

        visitor_team_players = list(
            TeamPlayer.objects.filter(team=visitor_team).annotate(
                name=models.F("player__name")
            )
        )

        initiative_team = home_team
        for minute in range(0, duration):
            initiative_team = (
                visitor_team if initiative_team == home_team else home_team
            )
            attackers = (
                home_team_players
                if initiative_team == home_team
                else visitor_team_players
            )
            defenders = (
                visitor_team_players
                if initiative_team == home_team
                else home_team_players
            )

            attackers = filter(lambda p: p.role == Role.OFFENCE, attackers)
            success = Match._attack(
                attackers, filter(lambda p: p.role == Role.DEFENCE, defenders)
            )
            if not success:
                continue

            success = Match._attack(
                attackers, filter(lambda p: p.role == Role.GOALIE, defenders)
            )
            if success:
                if initiative_team == home_team:
                    home_score += 1
                else:
                    visitor_score += 1
                highlights.append(
                    f"{initiative_team.name} scored! Score is {home_score}:{visitor_score}"
                )
            else:
                highlights.append(
                    f"{initiative_team.name} provided a successful attack! However, goal was not scored"
                )
        winner = (
            home_team
            if home_score > visitor_score
            else visitor_team if visitor_score > home_score else None
        )

        return Match.objects.create(
            home_team=home_team,
            visitor_team=visitor_team,
            winner=winner,
            highlights=highlights,
        )

    @staticmethod
    def _attack(attackers, defenders):
        attackers_power = sum(x.power for x in attackers) + 20
        defenders_power = sum(x.power for x in defenders)

        success_probability = 0.5 + (attackers_power - defenders_power) * 0.005
        success = random.random() < success_probability
        return success
