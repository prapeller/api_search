from django.urls import path

from core_apps.movies.v1 import views

urlpatterns = [
    path('movies/', views.FilmsListApi.as_view()),
    path('movies/<uuid:pk>/', views.FilmsDetailApi.as_view()),
]