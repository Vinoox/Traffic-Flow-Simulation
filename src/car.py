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
        self.startTime = time()* con.timeMultiplier
        self.endTime = 0
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
        self.pos = (self.x, self.y)

        self.speed = 0
        self.acceleration = 0.002
        self.maxSeed = 0.5

        self.end = 0
        self.travel_time = 0

        self.active = False
        self.passRoute = [self.startNode]
        self.stopTime=0
        self.pauseTime = 0
        self.updatedPath = False

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
        self.pos = (self.x, self.y)

    def stopTimeUpdate(self, time):
        self.existTime -= time

    def timeUpdate(self):
        self.existTime += (time() - self.currentTime) * con.timeMultiplier
        self.currentTime = time()

    def pausetimeUpdate(self):
        if self.speed == 0:
            self.pauseTime += (time() - self.currentstopTime) * con.timeMultiplier
            if self.junctionWaiting:
                self.junctionWaiting.carsWaiting.append(self)
        self.currentstopTime = time()

    def waitingTime(self):
        if self.speed == 0:
            self.pauseTime += (time() - self.currentTime) * con.timeMultiplier
        self.currentwaitTime = time()

    def waitingTimeUpdate(self, time2):
        self.pauseTime -= time2

    def removeFromJunctionWaitingList(self):
        if self.junctionWaiting:
            self.junctionWaiting.carsWaiting.remove(self)
            self.junctionWaiting = None

    def distance(self, pos1: tuple, pos2: tuple):
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1])**2) ** 0.5

    def distanceToLight(self):
        lightPos = self.road.traffic_light.position
        return self.distance(self.pos, lightPos)

    def distanceToNextCar(self):
        nextCarPos = self.road.cars_on_road[self.count - 1].pos
        return self.distance(self.pos, nextCarPos)

    def update(self):
        self.timeUpdate()
        self.waitingTime()

        junction = self.city.getJunction(self.nextNode)
        if self.road.traffic_light.state == 'red':
            if self not in junction.waiting_cars:
                junction.addCarWaitTime(self)

        if self.road.traffic_light.state == 'green':
            if self in junction.waiting_cars:
                junction.removeCarWaitTime(self)
                self.stopTime = self.stopTimeStart


        distanceToLight = self.distanceToLight()

        if self.count <= 0:
            if self.road.traffic_light.state == 'red':
                if distanceToLight < 7:
                    self.speed = 0
                elif distanceToLight < 20:
                    self.speed = max(0.01 * con.timeMultiplier, self.speed - self.acceleration * 4 * con.timeMultiplier)
                else:
                    self.speed = min(self.maxSeed * con.timeMultiplier, self.speed + self.acceleration * con.timeMultiplier)
            else:
                self.speed = min(self.maxSeed * con.timeMultiplier, self.speed + self.acceleration * con.timeMultiplier)

        else:
            distanceToNextCar = self.distanceToNextCar()

            if distanceToNextCar < 5:
                self.speed = 0
            elif distanceToNextCar < 20:
                self.speed = max(0.08 * con.timeMultiplier, self.speed - self.acceleration * 5 * con.timeMultiplier)
            else:
                self.speed = min(self.maxSeed * con.timeMultiplier, self.speed + self.acceleration * 2 * con.timeMultiplier)

        
        if self.count < 4:
            if distanceToLight < 7 and self.road.traffic_light.state == 'red':
                self.speed = 0
                return



        if abs(self.x - self.road.end[0]) < self.speed and abs(self.y - self.road.end[1]) < 10:
            if self.changed:
                self.pathIndex += 1
                self.changed = False

            if self.pathIndex < len(self.path) - 1:
                self.currentNode = self.path[self.pathIndex]
                self.nextNode = self.path[self.pathIndex + 1]
                road = self.city.getRoad((self.currentNode, self.nextNode))
                if len(road.cars_on_road) == 0 or self.distance(road.cars_on_road[-1].pos, road.start) > 3:
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