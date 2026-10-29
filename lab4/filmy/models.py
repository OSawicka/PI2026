from django.db import models


class Film(models.Model):
    tytul = models.CharField(max_length=200)
    rezyser = models.CharField(max_length=100)
    gatunek = models.CharField(max_length=50)
    rok_produkcji = models.IntegerField()
    opis = models.TextField()
    obejrzany = models.BooleanField(default=False)

    def __str__(self):
        return self.tytul