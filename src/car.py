from time import time
import random
from city_generator import City

class Car():
    def __init__(self, city: City):
        self.nodes = list(city.G.nodes())
        self.startNode = random.choice(self.nodes)
        self.endNode = random.choice(self.nodes)

        while self.endNode == self.startNode:
            self.endNode = random.choice(self.nodes)


        self.currentNode = self.startNode
        self.targetNode = self.endNode
        

        self.x = city.scalePos[self.startNode][0]
        self.y = city.scalePos[self.startNode][1]
        self.startTime = time()
        self.endTime = 0
        self.path = city.find_shortest_path(self.currentNode, self.targetNode)
        self.pathIndex = 0

        self.speed = 1

    def move(self, city: City):
        if self.pathIndex < len(self.path) - 1:
            # Pobierz aktualny i następny węzeł na ścieżce
            current_node = self.path[self.pathIndex]
            next_node = self.path[self.pathIndex + 1]

            # Współrzędne węzłów
            current_x, current_y = city.scalePos[current_node][0], city.scalePos[current_node][1]
            next_x, next_y = city.scalePos[next_node][0], city.scalePos[next_node][1]

            # Oblicz różnicę (wektor ruchu)
            dx = next_x - current_x
            dy = next_y - current_y

            # Oblicz dystans do następnego węzła
            distance = (dx**2 + dy**2)**0.5

            # Normalizacja wektora ruchu
            if distance != 0:
                dx /= distance
                dy /= distance

            # Przesuwanie pozycji samochodu
            self.x += dx * self.speed
            self.y += dy * self.speed

            # Sprawdź, czy dotarliśmy do kolejnego węzła
            if abs(self.x - next_x) < self.speed and abs(self.y - next_y) < self.speed:
                # Przeskocz do następnego węzła
                self.pathIndex += 1
                self.x, self.y = next_x, next_y

        else:
            # Jeśli dotarł do celu, zatrzymaj ruch
            self.currentNode = self.targetNode
            self.endTime = time()
    