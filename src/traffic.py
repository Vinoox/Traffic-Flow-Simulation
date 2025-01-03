from car import Car
import numpy as np
from time import time


class Traffic():
    def __init__(self):
        self.cars = []
        self.totalAmount = 0
        self.positions = np.empty((0, 2), dtype=float)  # Pusta tablica 2D
        self.vectors = np.empty((0, 2), dtype=float)    # Pusta tablica 2D
        self.speeds = np.empty((0,), dtype=float)       # Pusta tablica 1D
        self.maxSpeeds = np.empty((0,), dtype=float)    # Pusta tablica 1D
        self.accelerations = np.empty((0,), dtype=float)  # Pusta tablica 1D
        self.ends = np.empty((0, 2), dtype=float)       # Pusta tablica 2D
        self.finished = np.empty((0,), dtype=bool)      # Pusta tablica 1D

    def add(self, car: Car):
        # Dodanie obiektu Car do floty
        self.totalAmount += 1
        self.cars.append(car)

        # Rozszerzenie macierzy/wekotrów o dane nowego samochodu
        self.positions = np.vstack((self.positions, car.position))  # Dodaj pozycję
        self.vectors = np.vstack((self.vectors, car.vector))  # Dodaj wektor ruchu
        self.speeds = np.append(self.speeds, car.speed)  # Dodaj prędkość
        self.maxSpeeds = np.append(self.maxSpeeds, car.maxSpeed)  # Dodaj maks. prędkość
        self.accelerations = np.append(self.accelerations, car.acceleration)  # Dodaj przyspieszenie
        self.ends = np.vstack((self.ends, car.road.end))  # Dodaj pozycję końcową
        self.finished = np.append(self.finished, False)  # Ustaw status "nie zakończone"
    
    def move_all(self):
        # 1. Przyspieszanie
        self.speeds = np.minimum(self.speeds + self.accelerations, self.maxSpeeds)

        # 2. Aktualizacja pozycji
        self.positions += self.vectors * self.speeds[:, np.newaxis]

        # 3. Sprawdzenie, czy samochody dotarły do kolejnych węzłów
        distances_to_end = np.linalg.norm(self.positions - self.ends, axis=1)
        arrived = distances_to_end < self.speeds  # Maski dla samochodów, które dotarły do końca odcinka

        for i, car in enumerate(self.cars):
            if arrived[i] and not self.finished[i]:  # Samochód dotarł do węzła
                car.road.traffic -= 1  # Zmniejszenie ruchu na starej drodze
                car.pathIndex += 1

                if car.pathIndex + 1 < len(car.path):  # Jeśli są kolejne węzły
                    # Aktualizacja drogi i wektora ruchu
                    car.currentNode = car.path[car.pathIndex]
                    car.nextNode = car.path[car.pathIndex + 1]
                    car.road = car.city.getRoad((car.currentNode, car.nextNode))
                    car.roads.append(car.road)
                    car.road.traffic += 1
                    car.road.totalAmount += 1

                    # Aktualizacja pozycji, wektora i końcowej pozycji
                    self.positions[i] = np.array(car.road.start, dtype=float)
                    self.vectors[i] = np.array(car.road.getVector(), dtype=float)
                    self.ends[i] = np.array(car.road.end, dtype=float)
                else:
                    # Samochód dotarł do celu
                    car.endTime = time()
                    car.end = 1  # Oznacz samochód jako zakończony
                    self.finished[i] = True
                    print(f"Car {car.id} reached its destination in {car.totalTime()} seconds with avg speed {car.avgSpeed()}")
                
    def update(self):
        active_indices = ~self.finished  # Maski aktywnych samochodów (negacja tablicy `finished`)
        self.positions = self.positions[active_indices]
        self.vectors = self.vectors[active_indices]
        self.speeds = self.speeds[active_indices]
        self.maxSpeeds = self.maxSpeeds[active_indices]
        self.accelerations = self.accelerations[active_indices]
        self.ends = self.ends[active_indices]
        self.finished = self.finished[active_indices]
        self.cars = [self.cars[i] for i in range(len(self.cars)) if active_indices[i]]