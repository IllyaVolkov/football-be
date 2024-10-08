# Generated by Django 5.1 on 2024-08-24 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Source",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("base_url", models.URLField()),
                ("players_path", models.CharField(max_length=255)),
                (
                    "pagination",
                    models.CharField(
                        choices=[
                            ("N", "None"),
                            ("L", "LimitOffset"),
                            ("P", "PageNumber"),
                        ],
                        default="N",
                        max_length=1,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("weight", models.FloatField(help_text="Weight in Kg")),
                ("height", models.FloatField(help_text="Height in cm")),
                ("additional_data", models.JSONField(default=dict)),
                (
                    "unique_id",
                    models.CharField(
                        help_text="Unique id from source", max_length=255, unique=True
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="crawler.source"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
