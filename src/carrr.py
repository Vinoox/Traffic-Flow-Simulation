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
        self.startTime = time()* con.timeMultiplier
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

        self.speed = 0 * con.timeMultiplier
        self.end = 0
        self.travel_time = 0

        self.active = False

    def getSize(self):
        if self.active:
            return 5
        else:
            return 3

    def getColor(self):
        if self.active:
            return (255, 0, 255)
        else:
            return (51, 204, 255)

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
        Aktualizacja ruchu samochodu, uwzględniająca hamowanie przed światłami
        oraz innymi samochodami.
        """
        # Pobranie wektora kierunku ruchu
        dx, dy = self.vector

        # Sprawdzanie odległości od innych samochodów
        if self.count <= 0:
            self.speed = 0.5 * con.timeMultiplier
        else:
            nextCar = self.road.cars_on_road[self.count - 1]
            distance_to_car = ((self.x - nextCar.x) ** 2 + (self.y - nextCar.y) ** 2) ** 0.5

            if distance_to_car < 7:
                if (nextCar.x - self.x) * dx + (nextCar.y - self.y) * dy > 0:
                    self.speed = 0
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

        if self.count == 0:  # Pierwszy samochód
            if dot_product > 0:  # Samochód jedzie w stronę świateł
                if self.road.traffic_light.state == 'red':
                    if distance_to_light <= 25 and distance_to_light > 5:
                        deceleration = 0.2
                        self.speed -= deceleration * con.timeMultiplier
                        self.speed = max(self.speed, 0)

                    elif distance_to_light <= 5:
                        self.speed = 0

                if self.road.traffic_light.state == 'green' or distance_to_light > 30:
                    acceleration = 0.3
                    self.speed += acceleration * con.timeMultiplier
                    self.speed = min(self.speed, 3)



        # Dla pozostałych samochodów - hamowanie tylko gdy widzą, że inne auto stoi
        else:
            # sprawdzamy tylko pojazd przed aktualnym
            previous_car = self.road.cars_on_road[self.count - 1]

            if previous_car.speed == 0 and self.road.traffic_light.state == 'red':
                # Obliczamy odległość do samochodu przed nami
                distance_to_next_car = ((self.x - previous_car.x) ** 2 + (self.y - previous_car.y) ** 2) ** 0.5

                if distance_to_next_car <= 20 and distance_to_next_car > 5:
                    deceleration = 0.17
                    self.speed -= deceleration * con.timeMultiplier
                    self.speed = max(self.speed, 0)

                elif distance_to_next_car <= 5:
                    self.speed = 0

                elif distance_to_next_car > 30:
                    acceleration = 0.3
                    self.speed += acceleration * con.timeMultiplier
                    self.speed = min(self.speed, 3)

        # Sprawdzenie, czy dotarliśmy do kolejnego węzła
        if abs(self.x - self.road.end[0]) < self.speed and abs(self.y - self.road.end[1]) < 10:
            if self.changed:
                self.pathIndex += 1
                self.changed = False

            if self.pathIndex < len(self.path) - 1:
                self.currentNode = self.path[self.pathIndex]
                self.nextNode = self.path[self.pathIndex + 1]
                road = self.city.getRoad((self.currentNode, self.nextNode))
                if len(road.cars_on_road) == 0 or ((road.cars_on_road[-1].x - road.start[0]) ** 2 +
                                                   (road.cars_on_road[-1].y - road.start[1]) ** 2) ** 0.5 > 5:
                    self.removeFromRoad()
                    self.road = self.city.getRoad((self.currentNode, self.nextNode))
                    self.addToRoad()
                else:
                    self.speed = 0
            else:
                self.removeFromRoad()
                self.currentNode = self.endNode
                self.endTime = time()
                self.end = 1
                if self.end:
                    # Jeśli samochód dotarł do celu
                    self.travel_time = self.endTime - self.startTime
                    print(f"Car {self.id} reached destination: travel time= {self.travel_time}")