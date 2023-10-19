from django.urls import include, path

urlpatterns = [
    path('v1/', include('core_apps.movies.v1.urls')),
]
