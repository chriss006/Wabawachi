# Generated by Django 4.1.3 on 2022-11-25 16:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wineceller", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Hashtag",
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
                ("content", models.CharField(blank=True, max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Review",
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
                ("date", models.DateField(default=datetime.date.today)),
                (
                    "assessment",
                    models.CharField(
                        choices=[("좋음", "좋음"), ("보통", "보통"), ("나쁨", "나쁨")],
                        default="보통",
                        max_length=20,
                    ),
                ),
                (
                    "hashtag",
                    models.ManyToManyField(
                        blank=True, related_name="review", to="review.hashtag"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="review",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "wine",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="review",
                        to="wineceller.wine",
                    ),
                ),
            ],
            options={
                "verbose_name": "와인 리뷰",
                "verbose_name_plural": "와인 리뷰",
                "db_table": "wine_celler_review",
            },
        ),
    ]
