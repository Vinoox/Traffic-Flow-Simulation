# Traffic Flow Simulation

> Interaktywna symulacja ruchu drogowego w mieście generowanym proceduralnie, wykorzystująca teorię grafów i fizykę ruchu pojazdów.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pygame](https://img.shields.io/badge/Library-Pygame-yellow)
![NetworkX](https://img.shields.io/badge/Graph-NetworkX-green)

---

## 🇵🇱 O Projekcie

**Traffic Flow Simulation** to projekt badawczy wizualizujący dynamikę ruchu miejskiego. System generuje losową siatkę ulic (miasto), a następnie symuluje zachowanie setek niezależnych agentów (samochodów), które poruszają się zgodnie z zasadami ruchu drogowego, reagując na sygnalizację świetlną oraz inne pojazdy.

Aplikacja pozwala na interakcję w czasie rzeczywistym – użytkownik może zmieniać tempo symulacji, sterować sygnalizacją oraz badać parametry poszczególnych węzłów i pojazdów.

### Kluczowe Funkcjonalności

#### 🏙️ Generowanie Miasta i Grafy
* **Proceduralne Miasto:** Miasto jest generowane jako siatka (`Grid Graph`) przy użyciu biblioteki **NetworkX**.
* **Logika Węzłów:** Każde skrzyżowanie to węzeł grafu, a ulice to krawędzie posiadające wagi (długość).
* **Pathfinding:** Samochody znajdują optymalną trasę do celu wykorzystując **algorytm Dijkstry**.

#### 🚗 Fizyka i Sztuczna Inteligencja Pojazdów
* **Model Agenta:** Każdy samochód (`Car`) jest niezależnym bytem, który:
    * Śledzi pojazd przed sobą (zachowanie bezpiecznego odstępu).
    * Reaguje na sygnalizację świetlną (zwalnianie przed czerwonym, ruszanie na zielonym).
    * Posiada własne parametry fizyczne: prędkość, przyspieszenie (`0.002`), prędkość maksymalna.
* **Wykrywanie Kolizji:** Prosta logika zapobiegająca najeżdżaniu na inne pojazdy w obrębie tego samego segmentu drogi.

#### 🚦 Zarządzanie Ruchem
* **Inteligentne Skrzyżowania (`Junction`):** Skrzyżowania zarządzają cyklami świateł (Green/Orange/Red), sterując przepływem z dróg dolotowych.
* **Statystyki:** System zbiera dane o czasie oczekiwania (`WaitTime`) oraz czasie podróży dla każdego pojazdu.

### 🎮 Sterowanie i Interfejs (UI)

Symulacja obsługuje szereg skrótów klawiszowych pozwalających na manipulację światem:

| Klawisz | Akcja |
| :--- | :--- |
| **SPACJA** | Pauza / Wznowienie symulacji |
| **ESC** | Włącz / Wyłącz generowanie nowych pojazdów (Spawning) |
| **TAB** | Podświetlenie trasy wybranego pojazdu |
| **1 - 5** | Zmiana mnożnika prędkości czasu (Time Multiplier) |
| **R** | Wymuś CZERWONE światło na wszystkich skrzyżowaniach |
| **G** | Wymuś ZIELONE światło na wszystkich skrzyżowaniach |
| **C** | Wyczyść wszystkie samochody z mapy |
| **Mysz (LPM)** | Kliknij na samochód lub skrzyżowanie, aby zobaczyć statystyki |

---

## 🛠️ Tech Stack

Projekt został zrealizowany w języku **Python** z wykorzystaniem następujących bibliotek:

| Biblioteka | Zastosowanie |
| :--- | :--- |
| **Pygame** | Silnik graficzny, renderowanie okna, obsługa wejścia (klawiatura/mysz) |
| **NetworkX** | Struktury danych grafowych, generowanie siatki miasta, algorytmy najkrótszej ścieżki |
| **NumPy** | Obliczenia wektorowe i macierzowe (optymalizacja ruchu) |
| **Matplotlib** | Pomocnicze rysowanie struktury grafu (debugowanie) |

### Struktura Klas (Diagram Uproszczony)

```mermaid
classDiagram
    class City {
        +Graph G
        +list junctions
        +list roads
        +list cars
        +find_shortest_path()
        +update()
    }
    class Junction {
        +tuple id
        +list roadsIn
        +list roadsOut
        +update_light()
    }
    class Road {
        +tuple start
        +tuple end
        +TrafficLight traffic_light
        +list cars_on_road
    }
    class Car {
        +float speed
        +float acceleration
        +list path
        +move()
        +update()
        +distanceToNextCar()
    }
    class TrafficLight {
        +string state
        +int duration
    }

    City *-- Junction
    City *-- Road
    City o-- Car
    Road *-- TrafficLight
    Road o-- Car : contains
    Junction -- Road : connects
