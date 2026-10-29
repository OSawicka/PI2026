// Pobranie elementów strony
const przycisk = document.getElementById("wczytaj-filmy");
const listaFilmow = document.getElementById("lista-filmow");
const komunikat = document.getElementById("komunikat");
const filtrFilmow = document.getElementById("filtr-filmow");


// Pobieranie filmów z API Django
async function wczytajFilmy() {
    przycisk.disabled = true;
    komunikat.textContent = "Trwa pobieranie filmów...";
    listaFilmow.replaceChildren();

    try {
        // Odczytanie wybranego filtra
        const wybranyFiltr = filtrFilmow.value;

        // Przygotowanie adresu API
        let adresAPI = "/api/filmy/";

        if (wybranyFiltr === "obejrzane") {
            adresAPI += "?obejrzany=true";
        } else if (wybranyFiltr === "nieobejrzane") {
            adresAPI += "?obejrzany=false";
        }

        // Pobranie filmów z odpowiednim filtrem
        const response = await fetch(adresAPI);

        // Sprawdzenie odpowiedzi HTTP
        if (!response.ok) {
            throw new Error("Nie udało się pobrać filmów.");
        }

        // Odczyt danych JSON
        const dane = await response.json();

        // Sprawdzenie, czy API zwróciło listę
        if (!Array.isArray(dane.items)) {
            throw new Error("Nieprawidłowy format danych.");
        }

        // Obsługa pustej listy
        if (dane.items.length === 0) {
            komunikat.textContent = "Brak filmów do wyświetlenia.";
            return;
        }

        // Wyświetlanie filmów na stronie
        dane.items.forEach(function(film) {
            const karta = document.createElement("article");
            karta.classList.add("karta-filmu");

            const tytul = document.createElement("h3");
            tytul.textContent = film.tytul;

            const rezyser = document.createElement("p");
            rezyser.textContent = "Reżyser: " + film.rezyser;

            const gatunek = document.createElement("p");
            gatunek.textContent = "Gatunek: " + film.gatunek;

            const rok = document.createElement("p");
            rok.textContent = "Rok produkcji: " + film.rok_produkcji;

            const opis = document.createElement("p");
            opis.textContent = "Opis: " + (film.opis || "Brak opisu");

            const status = document.createElement("p");
            status.textContent = film.obejrzany
                ? "Status: Obejrzany"
                : "Status: Nieobejrzany";

            karta.append(tytul, rezyser, gatunek, rok, opis, status);
            listaFilmow.appendChild(karta);
        });

        // Usunięcie komunikatu o ładowaniu
        komunikat.textContent = "";

    } catch (error) {
        // Obsługa błędów
        komunikat.textContent = "Błąd: " + error.message;

    } finally {
        // Ponowne włączenie przycisku
        przycisk.disabled = false;
    }
}

// Uruchomienie pobierania po kliknięciu
przycisk.addEventListener("click", wczytajFilmy);