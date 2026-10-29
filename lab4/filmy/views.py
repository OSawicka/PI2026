from django.shortcuts import render
from django.http import JsonResponse
from .models import Film


# Wyświetlanie strony głównej
def strona_glowna(request):
    return render(request, 'filmy/index.html')


# API zwracające listę filmów w formacie JSON
def lista_filmow(request):
    filmy = Film.objects.all()

    # Odczytanie parametru filtrowania z adresu URL
    obejrzany = request.GET.get('obejrzany')

    if obejrzany is not None:
        if obejrzany.lower() == 'true':
            filmy = filmy.filter(obejrzany=True)
        elif obejrzany.lower() == 'false':
            filmy = filmy.filter(obejrzany=False)

    # Przygotowanie danych filmów
    dane = list(filmy.values(
        'id',
        'tytul',
        'rezyser',
        'gatunek',
        'rok_produkcji',
        'opis',
        'obejrzany'
    ))

    # Zwrócenie danych w formacie oczekiwanym przez JavaScript
    return JsonResponse({'items': dane})