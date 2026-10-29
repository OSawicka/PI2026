from django.shortcuts import render
from django.http import JsonResponse
from .models import Film


# Wyświetlanie strony głównej katalogu filmów
def strona_glowna(request):
    return render(request, 'filmy/index.html')


# API zwracające filmy w formacie JSON
def api_filmy(request):

    # Pobranie wszystkich filmów z bazy danych
    filmy = Film.objects.all().order_by('id')

    # Odczytanie parametru filtrowania z adresu URL
    obejrzany = request.GET.get('obejrzany')

    # Filtrowanie filmów za pomocą Django ORM
    if obejrzany == 'true':
        filmy = filmy.filter(obejrzany=True)

    elif obejrzany == 'false':
        filmy = filmy.filter(obejrzany=False)

    # Przygotowanie danych do odpowiedzi JSON
    dane = []

    for film in filmy:
        dane.append({
            'id': film.id,
            'tytul': film.tytul,
            'rezyser': film.rezyser,
            'gatunek': film.gatunek,
            'rok_produkcji': film.rok_produkcji,
            'opis': film.opis,
            'obejrzany': film.obejrzany,
        })

    return JsonResponse({'items': dane})