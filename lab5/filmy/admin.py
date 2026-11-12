from django.contrib import admin
from .models import Film
 
@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = (
        'tytul',
        'rezyser',
        'gatunek',
        'rok_produkcji',
        'ocena',
        'czas_trwania',
        'obejrzany',
    )
 
    list_filter = ('gatunek', 'obejrzany', 'ocena')
    search_fields = ('tytul', 'rezyser')
    list_editable = ('ocena', 'obejrzany')