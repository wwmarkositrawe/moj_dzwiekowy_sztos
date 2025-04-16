import pygame
import random
import time
import threading
from datetime import datetime
import os

# Inicjalizacja
pygame.init()
pygame.mixer.init()

# Wymiary okna
WIDTH, HEIGHT = 600, 400
okno = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mój Dźwiękowy Sztos")

# Czcionki
czcionka = pygame.font.SysFont(None, 80)
czcionka_mala = pygame.font.SysFont(None, 40)

# Kolory
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
CZERWONY = (255, 0, 0)

# Wczytanie obrazka
def wczytaj_grafike(nazwa_pliku):
    if os.path.exists(nazwa_pliku):
        grafika = pygame.image.load(nazwa_pliku)
        return pygame.transform.scale(grafika, (WIDTH, HEIGHT))
    else:
        print(f"Błąd: Plik {nazwa_pliku} nie istnieje!")
        input("Wciśnij Enter, aby kontynuować...")  # Zatrzymanie, żeby zobaczyć komunikat
        return None

grafika = wczytaj_grafike("C:/Users/mogulewicz/Documents/moj_dzwiekowy_sztos/grafika.jpg")

# Ścieżki dźwiękowe
def wczytaj_dzwiek(nazwa_pliku):
    if os.path.exists(nazwa_pliku):
        return nazwa_pliku
    else:
        print(f"Błąd: Plik {nazwa_pliku} nie istnieje!")
        input("Wciśnij Enter, aby kontynuować...")  # Zatrzymanie, żeby zobaczyć komunikat
        return None

nagranie1 = wczytaj_dzwiek("C:/Users/mogulewicz/Documents/moj_dzwiekowy_sztos/nagranie1.mp3")
nagranie2 = wczytaj_dzwiek("C:/Users/mogulewicz/Documents/moj_dzwiekowy_sztos/nagranie2.mp3")

# Flagi
uruchomione = threading.Event()  # Zamiast zmiennej Boolean, używamy Event
uruchomione.set()  # Event musi być ustawiony na "gotowe" na początku
zakonczone = threading.Event()  # To też Event

# Funkcja odtwarzająca dźwięk
def zagraj(plik):
    try:
        pygame.mixer.music.load(plik)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print(f"Błąd podczas odtwarzania pliku {plik}: {e}")
        input("Wystąpił błąd. Wciśnij Enter, aby kontynuować...")  # Dodajemy zatrzymanie, by przeczytać komunikat
        return False
    return True

# Konfetti
def konfetti():
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        kolor = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
        pygame.draw.circle(okno, kolor, (x, y), 5)
    pygame.display.flip()

# Zegar
def rysuj_zegar():
    teraz = datetime.now()
    tekst = czcionka_mala.render(teraz.strftime("%H:%M:%S"), True, CZARNY)
    okno.blit(tekst, (10, 10))

# Zadanie główne
def task():
    global uruchomione, zakonczone
    uruchomione.clear()  # Zatrzymanie dalszej interakcji przed rozpoczęciem
    liczba_powt = random.randint(1, 7)
    for _ in range(liczba_powt):
        if not zagraj(nagranie1):
            zakonczone.set()
            return  # Kończymy działanie wątku w przypadku błędu
    if not zagraj(nagranie2):
        zakonczone.set()
        return  # Kończymy działanie wątku w przypadku błędu
    konfetti()
    zakonczone.set()  # Sygnalizowanie, że zakończono
    uruchomione.set()  # Ponowne ustawienie, by przyciski mogły działać

# Główna pętla
dziala = True
while dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dziala = False
        elif event.type == pygame.MOUSEBUTTONDOWN and uruchomione.is_set():  # Uruchomienie tylko, gdy gotowe
            if zakonczone.is_set():
                zakonczone.clear()  # Resetowanie po kliknięciu „Zagraj jeszcze raz”
            threading.Thread(target=task).start()  # Uruchamianie nowego wątku

    if grafika:  # Upewniamy się, że obrazek został załadowany
        okno.blit(grafika, (0, 0))

    rysuj_zegar()

    if uruchomione.is_set() and not zakonczone.is_set():
        tekst = czcionka.render("Kliknij aby Start!", True, CZARNY)
        okno.blit(tekst, (80, HEIGHT // 2 - 40))

    if zakonczone.is_set():
        tekst = czcionka.render("Zagraj jeszcze raz", True, CZERWONY)
        okno.blit(tekst, (40, HEIGHT // 2 - 40))

    pygame.display.flip()
    pygame.time.Clock().tick(30)
