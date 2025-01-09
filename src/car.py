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
        self.currentTime = time()
        self.existTime = 0
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

        self.passRoute = [self.startNode]
        self.active = False

        self.updatedPath = False
        
    def getSize(self):
        if self.active: return 5
        else: return 3

    def getColor(self):
        if self.active:
            return (255, 0, 255)
        else: return (51, 204, 255)

    def removeFromRoad(self):
        for car in self.road.cars_on_road:
            car.count -= 1
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
        self.path = self.city.find_shortest_path(self.currentNode, self.endNode)
        self.pathIndex = 0
        self.updatedPath = True

    def move(self):
        dx, dy = self.vector
        self.x += dx * self.speed
        self.y += dy * self.speed

    def stopTimeUpdate(self, time):
        self.existTime -= time 

    def timeUpdate(self):
        self.existTime += (time() - self.currentTime) * con.timeMultiplier
        self.currentTime = time()

    def checkCarDistance(self):
        dx, dy = self.vector
        nextCar = self.road.cars_on_road[self.count - 1]
        if (nextCar.x - self.x) * dx + (nextCar.y - self.y) * dy < 7:
            return 0
        return 0.5 * con.timeMultiplier

    def checkLightDistance(self):
        dx, dy = self.vector
        # Obliczanie odległości do świateł (pozycja świateł)
        light_pos = self.road.traffic_light.position
        distance_to_light = ((self.x - light_pos[0]) ** 2 + (self.y - light_pos[1]) ** 2) ** 0.5

        # Sprawdzamy, czy samochód jedzie w stronę świateł
        direction_to_light = (light_pos[0] - self.x, light_pos[1] - self.y)
        dot_product = dx * direction_to_light[0] + dy * direction_to_light[1]

        # Jeśli jesteśmy blisko świateł i są czerwone, zatrzymujemy się
        if dot_product > 0 and distance_to_light < 5 and self.count <= 3:
            if self.road.traffic_light.state == 'red':
                return 0
            elif self.road.traffic_light.state == 'green':
                return 0.5 * con.timeMultiplier
        return  0.5 * con.timeMultiplier

    def moveToNextNode(self):
        # Sprawdzenie, czy dotarliśmy do kolejnego węzła
        if not self.changed or (abs(self.x - self.road.end[0]) < self.speed and abs(self.y - self.road.end[1]) < 10):
            if self.changed:
                self.pathIndex += 1; self.changed = False

            if self.pathIndex < len(self.path) - 1:  # Zapewniamy, że jest następny węzeł
                self.currentNode = self.path[self.pathIndex]
                self.updatePath()

                self.nextNode = self.path[self.pathIndex + 1]
                road = self.city.getRoad((self.currentNode, self.nextNode))
                if road.isSpace():
                    self.removeFromRoad()
                    self.passRoute.append(self.currentNode)
                    self.road = road
                    self.addToRoad()
                else:
                    self.speed = 0
            else:
                # Dotarliśmy do końca trasy
                self.removeFromRoad()
                self.currentNode = self.endNode
                self.end = 1

    def update(self):
        self.timeUpdate()
        self.updatedPath = False

        
        if self.count > 0:
            self.speed = self.checkCarDistance()
            if self.speed == 0: return

        if self.count <= 3:
            self.speed = self.checkLightDistance()

        self.moveToNextNode()