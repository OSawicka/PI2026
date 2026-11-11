from django.contrib import admin
from django.urls import path, include


# Główna lista adresów URL projektu Django.
urlpatterns = [

    # Panel administracyjny Django.
    path('admin/', admin.site.urls),

    # Dołączenie adresów URL aplikacji TaskBoard.
    path('', include('taskboard.urls')),
]