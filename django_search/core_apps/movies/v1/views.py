from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from core_apps.movies.models import FilmModel, RoleChoices


class FilmsQuerySetMixin:
    model = FilmModel
    http_method_names = ['get']

    def get_queryset(self):
        queryset = self.model.objects.prefetch_related('genres', 'persons')
        queryset = queryset.values('id', 'uuid', 'title', 'description', 'rating', 'type')
        queryset = queryset.annotate(
            creation_date=F('release_date'),
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg('persons__full_name', distinct=True,
                            filter=Q(filmpersonassociation__role=RoleChoices.ACTOR)),
            directors=ArrayAgg('persons__full_name', distinct=True,
                               filter=Q(filmpersonassociation__role=RoleChoices.DIRECTOR)),
            writers=ArrayAgg('persons__full_name', distinct=True,
                             filter=Q(filmpersonassociation__role=RoleChoices.WRITER)),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class FilmsListApi(FilmsQuerySetMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(self.get_queryset(),
                                                                         self.paginate_by)
        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset)}


class FilmsDetailApi(FilmsQuerySetMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        return kwargs.get('object')
