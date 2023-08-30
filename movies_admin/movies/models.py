from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

import uuid


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(_("created"), auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class TimeStampedMixin(CreatedAtMixin, UpdatedAtMixin):
    pass

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField("name", max_length=255)
    description = models.TextField("description", blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genre")

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmworkTypes(models.TextChoices):
        MOVIE = "MOVIE", _("movie")
        TV_SHOW = "TV_SHOW", _("tv show")

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))
    creation_date = models.DateField(_("creation date"))
    type = models.CharField(
        _("type"), choices=FilmworkTypes.choices, default=FilmworkTypes.MOVIE
    )
    rating = models.FloatField(
        "rating", blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    genres = models.ManyToManyField(
        "Genre", through="GenreFilmwork", verbose_name=_("genres")
    )
    file_path = models.FileField(_("file"), blank=True, null=True, upload_to="movies/")

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("filmwork")
        verbose_name_plural = _("filmworks")

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin, CreatedAtMixin):
    film_work = models.ForeignKey(
        "Filmwork", on_delete=models.CASCADE, verbose_name=_("filmwork")
    )
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE, verbose_name=_("genre")
    )

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("genre filmwrok")
        verbose_name_plural = _("genres filmwroks")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "genre"], name="unique_filmwork_genre"
            )
        ]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full name"), max_length=120)
    film_work = models.ManyToManyField(
        "Filmwork", through="PersonFilmwork", verbose_name=_("filmwork")
    )

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("persons")
        

    def __str__(self) -> str:
        return self.full_name


class PersonFilmwork(UUIDMixin, CreatedAtMixin):
    film_work = models.ForeignKey(
        "Filmwork", on_delete=models.CASCADE, verbose_name=_("filmwork")
    )
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE, verbose_name=_("person")
    )
    role = models.TextField("role", null=True)

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("person filmwork")
        verbose_name_plural = _("persons filmworks")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work", "person", "role"], name="unique_filmwork_person_role"
            )
        ]
