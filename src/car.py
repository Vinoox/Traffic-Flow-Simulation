from time import time
import random
from city_generator import City
import config as con


class Car:
    def __init__(self, city: City, id, startNode=None, endNode=None):
        self.city = city
        self.id = id
        self.nodes = list(city.G.nodes())
        if startNode is not None:
            self.nodes.remove(startNode)
        if endNode is not None:
            self.nodes.remove(endNode)

        if startNode is None:
            self.startNode = random.choice(self.nodes)
            self.nodes.remove(self.startNode)
        else:
            self.startNode = startNode

        if endNode is None:
            self.endNode = random.choice(self.nodes)
        else:
            self.endNode = endNode


        self.currentNode = self.startNode
        self.startTime = time()
        self.endTime = 0
        self.path = self.city.find_shortest_path(self.startNode, self.endNode)

        self.pathIndex = 0
        self.nextNode = self.path[1]

        self.changed = True

        self.road = city.getRoad((self.currentNode, self.nextNode))
        self.count = self.road.traffic
        self.vector = self.road.getVector()
        self.x = self.road.start[0] + self.vector[0] * 10
        self.y = self.road.start[1] + self.vector[1] * 10
        pos = (self.x, self.y)

        self.speed = 0.5 * con.timeMultiplier
        self.end = 0

        self.active = False


    def reduceTraffic(self):
        for car in self.road.cars_on_road:
            car.count -= 1

    def removeFromRoad(self):
        self.reduceTraffic()
        self.road.traffic -= 1
        self.road.cars_on_road.pop(0)

    def addToRoad(self):
        self.changed = True
        self.count = self.road.traffic
        self.road.traffic += 1
        self.road.totalTraffic += 1
        self.road.cars_on_road.append(self)
        self.vector = self.road.getVector()
        self.x, self.y = self.road.start[0], self.road.start[1]

    def updatePath(self):
        self.newPath = self.city.find_shortest_path(self.currentNode, self.endNode)
        self.path = self.city.find_shortest_path(self.currentNode, self.endNode)
        self.pathIndex = 0

    def move(self):
        dx, dy = self.vector
        self.x += dx * self.speed
        self.y += dy * self.speed

    def update(self):
        """
        Ruch samochodu z uwzględnieniem innych samochodów na tej samej drodze
        oraz sygnalizacji świetlnej.
        """
        # Pobranie wektora kierunku ruchu
        dx, dy = self.vector

        # Sprawdzanie odległości od innych samochodów
        if self.count <= 0:
            self.speed = 0.5 * con.timeMultiplier
        else:
            nextCar = self.road.cars_on_road[self.count - 1]
            distance_to_car = ((self.x - nextCar.x) ** 2 + (self.y - nextCar.y) ** 2) ** 0.5
            # Zatrzymujemy się tylko wtedy, gdy odległość jest bardzo mała
            # i inne auto blokuje drogę
            if distance_to_car < 7:
                if (nextCar.x - self.x) * dx + (nextCar.y - self.y) * dy > 0:
                    self.speed = 0  # Zatrzymujemy się, czekamy, aż będzie miejsce
                    return
                else:
                    self.speed = 0.5 * con.timeMultiplier
            else:
                self.speed = 0.5 * con.timeMultiplier

        # Obliczanie odległości do świateł (pozycja świateł)
        light_pos = self.road.traffic_light.position
        distance_to_light = ((self.x - light_pos[0]) ** 2 + (self.y - light_pos[1]) ** 2) ** 0.5

        # Sprawdzamy, czy samochód jedzie w stronę świateł
        direction_to_light = (light_pos[0] - self.x, light_pos[1] - self.y)
        dot_product = dx * direction_to_light[0] + dy * direction_to_light[1]

        # Jeśli jesteśmy blisko świateł i są czerwone, zatrzymujemy się
        if dot_product > 0 and distance_to_light < 5 and self.count <= 5:
            if self.road.traffic_light.state == 'red':
                self.speed = 0 # Czekamy na zielone światło
            elif self.road.traffic_light.state == 'green':
                # Możemy ruszyć, jeśli światło jest zielone i jesteśmy blisko
                self.speed = 0.5 * con.timeMultiplier



        # Sprawdzenie, czy dotarliśmy do kolejnego węzła
        if abs(self.x - self.road.end[0]) < self.speed and abs(self.y - self.road.end[1]) < 10 and self.count <= 0:
            if self.changed:
                self.pathIndex += 1; self.changed = False

            if self.pathIndex < len(self.path) - 1:  # Zapewniamy, że jest następny węzeł
                self.currentNode = self.path[self.pathIndex]
                # self.updatePath()
                self.nextNode = self.path[self.pathIndex + 1]
                road = self.city.getRoad((self.currentNode, self.nextNode))
                if len(road.cars_on_road) != 0: 
                    distance_to_last_car = ((road.cars_on_road[-1].x - road.start[0]) ** 2 + (road.cars_on_road[-1].y - road.start[1]) ** 2) ** 0.5
                if len(road.cars_on_road) == 0 or distance_to_last_car > 5:
                    self.removeFromRoad()
                    self.road = self.city.getRoad((self.currentNode, self.nextNode))
                    self.addToRoad()
                else:
                    self.speed = 0
            else:
                # Dotarliśmy do końca trasy
                self.removeFromRoad()
                self.currentNode = self.endNode
                self.endTime = time()  # Rejestrujemy czas zakończenia
                self.end = 1  # Oznaczamy, że dotarliśmy do celu