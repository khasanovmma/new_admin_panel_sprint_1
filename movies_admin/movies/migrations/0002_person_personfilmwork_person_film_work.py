# Generated by Django 4.2.4 on 2023-08-07 04:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "modified",
                    models.DateTimeField(auto_now=True, verbose_name="modified"),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "full_name",
                    models.CharField(max_length=120, verbose_name="full name"),
                ),
            ],
            options={
                "verbose_name": "person",
                "verbose_name_plural": "persons",
                "db_table": 'content"."person',
            },
        ),
        migrations.CreateModel(
            name="PersonFilmwork",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("role", models.TextField(null=True, verbose_name="role")),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="created"),
                ),
                (
                    "film_work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.filmwork",
                        verbose_name="filmwork",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movies.person",
                        verbose_name="person",
                    ),
                ),
            ],
            options={
                "verbose_name": "person filmwork",
                "verbose_name_plural": "persons filmworks",
                "db_table": 'content"."person_film_work',
            },
        ),
        migrations.AddField(
            model_name="person",
            name="film_work",
            field=models.ManyToManyField(
                through="movies.PersonFilmwork",
                to="movies.filmwork",
                verbose_name="filmwork",
            ),
        ),
    ]
