from time import time
import random
from city_generator import City


class Car:
    def __init__(self, city: City):
        self.city = city

        #choose start and end node
        self.nodes = list(city.G.nodes())
        self.startNode = random.choice(self.nodes)
        self.nodes.remove(self.startNode)
        self.endNode = random.choice(self.nodes)


        self.currentNode = self.startNode
        self.startTime = time()
        self.endTime = 0
        self.path = city.find_shortest_path(self.startNode, self.endNode)

        self.pathIndex = 0
        self.nextNode = self.path[1]

        self.road = city.getRoad((self.currentNode, self.nextNode))
        self.road.traffic += 1
        self.road.cars_on_road.append(self)
        self.x = self.road.start[0]
        self.y = self.road.start[1]

        self.speed = 0.5
        self.end = 0



    def move(self):
        """
        Ruch samochodu z uwzględnieniem innych samochodów na tej samej drodze
        oraz sygnalizacji świetlnej.
        """
        # Pobranie wektora kierunku ruchu
        self.vector = self.road.getVector()
        dx, dy = self.vector

        # Obliczanie odległości do świateł (pozycja świateł)
        light_pos = self.road.traffic_light.position
        distance_to_light = ((self.x - light_pos[0]) ** 2 + (self.y - light_pos[1]) ** 2) ** 0.5

        # Sprawdzamy, czy samochód jedzie w stronę świateł
        direction_to_light = (light_pos[0] - self.x, light_pos[1] - self.y)
        dot_product = dx * direction_to_light[0] + dy * direction_to_light[1]

        # Jeśli jesteśmy blisko świateł i są czerwone, zatrzymujemy się
        if dot_product > 0 and distance_to_light < 15:
            if self.road.traffic_light.state == 'red':
                return  # Czekamy na zielone światło
            elif self.road.traffic_light.state == 'green':
                # Możemy ruszyć, jeśli światło jest zielone i jesteśmy blisko
                pass

        # Sprawdzanie odległości od innych samochodów
        for other_car in self.road.cars_on_road:
            if other_car == self:
                continue  # Pomijamy sam siebie

            distance_to_car = ((self.x - other_car.x) ** 2 + (self.y - other_car.y) ** 2) ** 0.5
            # Zatrzymujemy się tylko wtedy, gdy odległość jest bardzo mała
            # i inne auto blokuje drogę
            if distance_to_car < 10:
                if other_car.x > self.x:  # Inne auto jest przed nami
                    return  # Zatrzymujemy się, czekamy, aż będzie miejsce

        # Jeśli światło jest zielone i nie ma innych przeszkód, poruszamy się
        self.x += dx * self.speed
        self.y += dy * self.speed

        # Sprawdzenie, czy dotarliśmy do kolejnego węzła
        if abs(self.x - self.road.end[0]) < self.speed and abs(self.y - self.road.end[1]) < 10:
            self.road.traffic -= 1  # Zmniejszamy ruch na drodze
            self.road.cars_on_road.remove(self)
            self.pathIndex += 1
            if self.pathIndex + 1 < len(self.path):  # Zapewniamy, że jest następny węzeł
                self.currentNode = self.path[self.pathIndex]
                self.nextNode = self.path[self.pathIndex + 1]
                self.road = self.city.getRoad((self.currentNode, self.nextNode))
                self.road.traffic += 1
                self.road.cars_on_road.append(self)
                self.x, self.y = self.road.start[0], self.road.start[1]
            else:
                # Dotarliśmy do końca trasy
                self.currentNode = self.endNode
                self.endTime = time()  # Rejestrujemy czas zakończenia
                self.end = 1  # Oznaczamy, że dotarliśmy do celu