from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.urls import path
from django.utils.translation import gettext_lazy as _
from .models import GenreModel, FilmModel, FilmGenreAssociation, FilmPersonAssociation, PersonModel


class UUIDAdmin(admin.ModelAdmin):
    # def get_object(self, request, object_id, from_field=None):
    #     queryset = self.get_queryset(request)
    #     model = queryset.model
    #     if from_field is None:
    #         from_field = model._meta.pk.name
    #     return get_object_or_404(queryset, **{from_field: object_id})
    #
    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path('<uuid:object_id>/change/', staff_member_required(self.change_view),
    #              name='%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name)),
    #     ]
    #     return custom_urls + urls
    pass


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
class FilmAdmin(UUIDAdmin):
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
class GenreAdmin(UUIDAdmin):
    list_display = ('name', 'short_description')
    list_filter = ('name',)
    search_fields = ('name', 'description', 'uuid')


@admin.register(PersonModel)
class PersonAdmin(UUIDAdmin):
    inlines = (PersonFilmInline,)
    list_display = ('full_name', 'first_name', 'last_name')
    search_fields = ('full_name', 'uuid')
