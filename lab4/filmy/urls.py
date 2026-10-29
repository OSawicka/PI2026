from django.urls import path
from . import views

urlpatterns = [
    path('', views.strona_glowna, name='strona_glowna'),
    path('api/filmy/', views.api_filmy, name='api_filmy'),
]