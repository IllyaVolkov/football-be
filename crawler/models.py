from django.db import models

from utils.models import BaseModel


class Pagination(models.TextChoices):
    NONE = "N", "None"
    LIMIT_OFFSET = "L", "LimitOffset"
    PAGE_NUMBER = "P", "PageNumber"


class Source(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    base_url = models.URLField()
    players_path = models.CharField(max_length=255)
    pagination = models.CharField(
        max_length=1, choices=Pagination.choices, default=Pagination.NONE
    )

    def __str__(self):
        return self.name


class Player(BaseModel):
    name = models.CharField(max_length=255)
    weight = models.FloatField(help_text="Weight in Kg")
    height = models.FloatField(help_text="Height in cm")
    additional_data = models.JSONField(default=dict)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    unique_id = models.CharField(
        max_length=255, unique=True, help_text="Unique id from source"
    )

    def __str__(self):
        return self.name
