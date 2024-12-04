from time import time
import random
from city_generator import City

class Car():
    def __init__(self, city: City):
        self.city = city
        self.nodes = list(city.G.nodes())
        self.startNode = random.choice(self.nodes)
        self.endNode = random.choice(self.nodes)

        while self.endNode == self.startNode:
            self.endNode = random.choice(self.nodes)


        self.currentNode = self.startNode
        self.startTime = time()
        self.endTime = 0
        self.path = city.find_shortest_path(self.startNode, self.endNode)
        print(self.path)

        self.pathIndex = 0
        self.nextNode = self.path[1]
                
        self.road = city.getRoad((self.currentNode, self.nextNode))
        self.road.traffic += 1
        self.x = self.road.start[0]
        self.y = self.road.start[1]

        self.speed = 0.5
        self.end = 0

    def move(self):
        self.vector = self.road.getVector()
        dx, dy = self.vector
        
        # Przesuwanie pozycji samochodu
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Sprawdź, czy dotarliśmy do kolejnego węzła
        if abs(self.x - self.road.end[0]) < self.speed and abs(self.y - self.road.end[1]) < 10:
            # Przeskocz do następnego węzła
            self.road.traffic -= 1
            self.pathIndex += 1
            if self.pathIndex + 1 < len(self.path):  # Zapewniamy, że jest następny węzeł
                self.currentNode = self.path[self.pathIndex]
                self.nextNode = self.path[self.pathIndex + 1]
                self.road = self.city.getRoad((self.currentNode, self.nextNode))
                self.road.traffic += 1
                self.x, self.y = self.road.start[0], self.road.start[1]
            else:
                self.currentNode = self.endNode
                self.endTime = time()  # Czas zakończenia
                self.end = 1  # Oznaczamy, że dotarł do celu