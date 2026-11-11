from django.urls import path
from . import views


# Adresy URL obsługiwane przez aplikację TaskBoard.
urlpatterns = [

    # Strona główna aplikacji TaskBoard.
    path("", views.index, name="index"),

    # Pobieranie listy zadań i dodawanie nowych zadań (GET, POST).
    path("api/tasks/", views.tasks_api, name="tasks_api"),

    # Zmiana statusu i usuwanie konkretnego zadania (PATCH, DELETE).
    path("api/tasks/<int:task_id>/", views.task_detail_api, name="task_detail_api"),
]