import uuid

from django.contrib import admin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, connection
from django.utils.translation import gettext_lazy as _


class IdentifiedWithIDPrimary(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)

    class Meta:
        abstract = True


class IdentifiedWithUuidNotPrimary(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.uuid is None:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)


class Created(models.Model):
    created_at = models.DateTimeField(_('created in db'), auto_now_add=True)

    class Meta:
        abstract = True


class Updated(models.Model):
    updated_at = models.DateTimeField(_('modified in db'), auto_now=True, null=True)

    class Meta:
        abstract = True


# class IdentifiedWithIDNotPrimary(models.Model):
#     id = models.IntegerField(unique=True, null=True, blank=True)
#
#     class Meta:
#         abstract = True
#
#     def save(self, *args, **kwargs):
#         if self.id is None:
#             with connection.cursor() as cursor:
#                 sequence_name = f"{self.__class__.__name__.lower()}_integer_id_seq"
#                 cursor.execute(f"SELECT nextval('{sequence_name}')")
#                 self.id = cursor.fetchone()[0]
#         super().save(*args, **kwargs)


class TypeChoices(models.TextChoices):
    MOVIE = 'movie', _('Movie')
    SHORT = 'short', _('Short')
    TV_SERIES = 'tv-series', _('TV-Series')
    CARTOON = 'cartoon', _('Cartoon')


class RoleChoices(models.TextChoices):
    ACTOR = 'actor', _('Actor')
    WRITER = 'writer', _('Writer')
    DIRECTOR = 'director', _('Director')


class GenreModel(IdentifiedWithIDPrimary, IdentifiedWithUuidNotPrimary, Created, Updated):
    name = models.CharField(_('name'), null=False, max_length=255)
    description = models.TextField(_('description'), null=True)

    @admin.display(description=_('short description'))
    def short_description(self):
        if self.description and len(self.description) > 30:
            return self.description[:30] + '...'
        return self.description

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class FilmModel(IdentifiedWithIDPrimary, IdentifiedWithUuidNotPrimary, Created, Updated):
    title = models.CharField(_('title'), null=False, max_length=255, db_index=True)
    description = models.TextField(_('description'), null=True)
    release_date = models.DateField(_('release date'), null=True, blank=True, db_index=True)
    file_path = models.TextField(_('file_path'), null=True)
    imdb_rating = models.FloatField(_('imdb rating'), null=True, blank=True,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(10)])
    type = models.CharField(_('type'), null=False, max_length=255, choices=TypeChoices.choices, db_index=True)
    genres = models.ManyToManyField('GenreModel', through='FilmGenreAssociation')
    persons = models.ManyToManyField('PersonModel', through='FilmPersonAssociation')

    @admin.display(description=_('short description'))
    def short_description(self):
        if self.description and len(self.description) > 30:
            return self.description[:30] + '...'
        return self.description

    class Meta:
        db_table = "content\".\"film"
        verbose_name = _('Film work')
        verbose_name_plural = _('Film works')

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #     requests.post(
    #         f'http://{settings.API_SEARCH_HOST}:{settings.API_SEARCH_PORT}'
    #         f'/api/v1/etl/extract-from-postgres-load-to-elastic-by-id-list',
    #         json=[self.uuid.hex])

    def __str__(self):
        return self.title


class PersonModel(IdentifiedWithIDPrimary, IdentifiedWithUuidNotPrimary, Created, Updated):
    full_name = models.CharField(_('full name'), max_length=255)
    films = models.ManyToManyField(FilmModel, through='FilmPersonAssociation')

    @admin.display(description=_('first name'))
    def first_name(self):
        names = self.full_name.split(' ')
        return names[0]

    @admin.display(description=_('last name'))
    def last_name(self):
        names = self.full_name.split(' ')
        if len(names) > 1:
            return names[1]
        return names

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class FilmGenreAssociation(IdentifiedWithIDPrimary, Created):
    film = models.ForeignKey('FilmModel', to_field='uuid', on_delete=models.CASCADE, db_column='film_uuid')
    genre = models.ForeignKey('GenreModel', to_field='uuid', on_delete=models.CASCADE, db_column='genre_uuid')

    class Meta:
        db_table = "content\".\"film_genre"
        unique_together = (('film', 'genre'),)


class FilmPersonAssociation(IdentifiedWithIDPrimary, Created):
    film = models.ForeignKey('FilmModel', to_field='uuid', on_delete=models.CASCADE, db_column='film_uuid')
    person = models.ForeignKey('PersonModel', to_field='uuid', on_delete=models.CASCADE, db_column='person_uuid')
    role = models.CharField(_('role'), max_length=255, choices=RoleChoices.choices)

    class Meta:
        db_table = "content\".\"film_person"
        unique_together = (('film', 'person', 'role'),)
