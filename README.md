# Aplikacja IP Checker

## Struktura plików:

### Główne pliki:
- `main.py` - Plik startowy aplikacji
- `app.py` - Konfiguracja Flask i bazy danych
- `routes.py` - Obsługa adresów URL
- `models.py` - Model bazy danych do zapisywania wizyt

### Szablony (templates):
- `templates/index.html` - Strona główna pokazująca IP
- `templates/admin/visits.html` - Panel administratora z historią wizyt

### Style i skrypty:
- `static/css/custom.css` - Style wyglądu strony
- `static/js/ip.js` - Skrypt do kopiowania IP

### Pliki konfiguracyjne:
- `.replit` - Konfiguracja Replit
- `pyproject.toml` - Zależności Pythona
- `replit.nix` - Konfiguracja środowiska

## Co robi każdy plik:

1. **main.py**
   - Uruchamia serwer Flask
   - Konfiguruje logowanie

2. **app.py**
   - Tworzy aplikację Flask
   - Konfiguruje bazę danych PostgreSQL
   - Inicjalizuje połączenie z bazą

3. **routes.py**
   - Obsługuje stronę główną ("/")
   - Wykrywa IP odwiedzającego
   - Obsługuje panel admina ("/admin/visits")

4. **models.py**
   - Definiuje model Visit do zapisywania:
     - adresu IP
     - czasu wizyty

5. **templates/index.html**
   - Wyświetla IP użytkownika
   - Umożliwia kopiowanie IP
   - Ma przycisk odświeżania

6. **templates/admin/visits.html**
   - Pokazuje tabelę wszystkich wizyt
   - Wyświetla IP i czas każdej wizyty

7. **static/css/custom.css**
   - Style dla strony (kolory, układ)
   - Responsywny design

8. **static/js/ip.js**
   - Obsługa kopiowania IP do schowka
   - Odświeżanie strony
