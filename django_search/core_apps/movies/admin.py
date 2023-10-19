from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import GenreModel, FilmModel, FilmGenreAssociation, FilmPersonAssociation, PersonModel


class FilmGenreInline(admin.TabularInline):
    model = FilmGenreAssociation
    extra = 1
    verbose_name = _('Genre of Film work')
    verbose_name_plural = _('Genres of Film work')
    autocomplete_fields = ('genre',)


class FilmPersonInline(admin.TabularInline):
    model = FilmPersonAssociation
    extra = 1
    verbose_name = _('Person of Film work')
    verbose_name_plural = _('Persons of Film work')
    autocomplete_fields = ('person',)


@admin.register(FilmModel)
class FilmAdmin(admin.ModelAdmin):
    inlines = (FilmGenreInline, FilmPersonInline)
    list_display = ('title', 'type', 'release_date', 'imdb_rating', 'created_at', 'updated_at', 'short_description')
    list_filter = ('title', 'type', 'release_date', 'imdb_rating', 'created_at')
    search_fields = ('title', 'description', 'uuid')


class PersonFilmInline(admin.TabularInline):
    model = FilmPersonAssociation
    extra = 1
    verbose_name = _('Film work of person')
    verbose_name_plural = _('Film works of person')


@admin.register(GenreModel)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description')
    list_filter = ('name',)
    search_fields = ('name', 'description', 'uuid')


@admin.register(PersonModel)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmInline,)
    list_display = ('full_name', 'first_name', 'last_name')
    search_fields = ('full_name', 'uuid')
