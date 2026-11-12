from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
 
 
class Film(models.Model):
    tytul = models.CharField(max_length=200)
    rezyser = models.CharField(max_length=100)
    gatunek = models.CharField(max_length=100, default="Nieokreślony")
    rok_produkcji = models.IntegerField()
    opis = models.TextField(blank=True)
    obejrzany = models.BooleanField(default=False)
 
    # Nowe pola - Laboratorium 5
    ocena = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    czas_trwania = models.PositiveIntegerField(
        null=True,
        blank=True
    )
 
    def __str__(self):
        return self.tytul