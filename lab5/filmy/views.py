 
from django.shortcuts import render
from django.http import JsonResponse
from .models import Film
 
 
# Wyświetlanie strony głównej
def strona_glowna(request):
    return render(request, 'filmy/index.html')
 
 
# API zwracające listę filmów w formacie JSON
def lista_filmow(request):
 
    # 1. Pobranie wszystkich filmów posortowanych alfabetycznie
    filmy = Film.objects.all().order_by('tytul')
 
    # 2. Filtrowanie filmów według statusu obejrzenia
    obejrzany = request.GET.get('obejrzany')
 
    if obejrzany is not None:
        if obejrzany.lower() == 'true':
            filmy = filmy.filter(obejrzany=True)
        elif obejrzany.lower() == 'false':
            filmy = filmy.filter(obejrzany=False)
 
    # 3. Ograniczenie wyników do trzech filmów
    limit = request.GET.get('limit')
 
    if limit == '3':
        filmy = filmy[:3]
 
    # Przygotowanie danych filmów
    dane = list(filmy.values(
        'id',
        'tytul',
        'rezyser',
        'gatunek',
        'rok_produkcji',
        'opis',
        'obejrzany',
        'ocena',
        'czas_trwania'
    ))
 
    # Zwrócenie danych w formacie oczekiwanym przez JavaScript
    return JsonResponse({'items': dane})
 