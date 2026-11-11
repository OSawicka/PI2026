import json

from django.http import JsonResponse
from django.shortcuts import render
from .models import Task

# Widok wyświetlający stronę główną aplikacji TaskBoard.
def index(request):

    # Wczytujemy szablon HTML z folderu templates/lab3.
    return render(request, "lab3/index.html")

# API obsługujące pobieranie i dodawanie zadań.
def tasks_api(request):

    # GET - pobieranie wszystkich zadań z bazy danych.
    if request.method == "GET":

        # Pobieramy zadania od najnowszego do najstarszego.
        tasks = Task.objects.all().order_by("-created_at")

        # Przygotowujemy listę zadań do przesłania jako JSON.
        tasks_list = []

        for task in tasks:
            tasks_list.append({
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
            })

        return JsonResponse(tasks_list, safe=False)

    # POST - dodawanie nowego zadania do bazy danych.
    elif request.method == "POST":

        # Odczytujemy dane JSON przesłane przez JavaScript.
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse(
                {"error": "Nieprawidłowe dane JSON."},
                status=400
            )

        # Pobieramy tytuł zadania i usuwamy zbędne spacje.
        title = data.get("title", "")

        if not isinstance(title, str):
            return JsonResponse(
                {"error": "Tytuł zadania musi być tekstem."},
                status=400
            )

        title = title.strip()

        # Sprawdzamy, czy użytkownik podał tytuł.
        if not title:
            return JsonResponse(
                {"error": "Tytuł zadania nie może być pusty."},
                status=400
            )

        # Sprawdzamy maksymalną długość tytułu.
        if len(title) > 200:
            return JsonResponse(
                {"error": "Tytuł może mieć maksymalnie 200 znaków."},
                status=400
            )

        # Tworzymy nowe zadanie w bazie danych.
        task = Task.objects.create(title=title)

        # Zwracamy dane utworzonego zadania.
        return JsonResponse({
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
        }, status=201)

    # Obsługa innych metod HTTP.
    return JsonResponse(
        {"error": "Niedozwolona metoda HTTP."},
        status=405
    )

# API obsługujące zmianę statusu i usuwanie pojedynczego zadania.
def task_detail_api(request, task_id):

    # Szukamy zadania o podanym identyfikatorze.
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse(
            {"error": "Nie znaleziono zadania."},
            status=404
        )

    # PATCH - zmiana statusu ukończenia zadania.
    if request.method == "PATCH":

        # Odczytujemy dane JSON przesłane przez JavaScript.
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse(
                {"error": "Nieprawidłowe dane JSON."},
                status=400
            )

        # Sprawdzamy, czy przesłano wartość true lub false.
        completed = data.get("completed")

        if not isinstance(completed, bool):
            return JsonResponse(
                {"error": "Pole completed musi mieć wartość true lub false."},
                status=400
            )

        # Zmieniamy status zadania i zapisujemy go w bazie.
        task.completed = completed
        task.save()

        # Zwracamy zaktualizowane dane zadania.
        return JsonResponse({
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
        })

    # DELETE - usunięcie zadania z bazy danych.
    elif request.method == "DELETE":

        # Usuwamy wskazane zadanie.
        task.delete()

        # Zwracamy potwierdzenie usunięcia.
        return JsonResponse({
            "message": "Zadanie zostało usunięte."
        })

    # Obsługa pozostałych metod HTTP.
    return JsonResponse(
        {"error": "Niedozwolona metoda HTTP."},
        status=405
    )