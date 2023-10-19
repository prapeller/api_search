from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('api/', include('core_apps.movies.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
