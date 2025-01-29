from time import time
import config as con

color = {'white' : (255, 255, 255),
         'blue': (0, 0, 255)}

class Junction:
    def __init__(self, id: tuple, pos: tuple):
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.roadsFrom = []
        self.roadsTo = []
        self.time = time()
        self.initial = True
        self.counter = 0

        self.active = False
        self.start = False
        self.end = False

        self.totalStopTime = 0
        self.carsPassed = 0

        # self.waiting_cars = []

    def getColor(self):
        if self.active:
            return (255, 255, 0)  # Blue if active
        return (255, 255, 255)  # White otherwise

    def pos(self):
        return (self.x, self.y)

    def update_light(self):
        if self.active:
            if self.roadsTo[self.counter].trafficColor == "orange":
                cycleDuration = self.roadsTo[self.counter].traffic_light.cycle_duration * 1.5
            elif self.roadsTo[self.counter].trafficColor == "red":
                cycleDuration = self.roadsTo[self.counter].traffic_light.cycle_duration * 2
            else: cycleDuration = self.roadsTo[self.counter].traffic_light.cycle_duration / 3
        else: cycleDuration = self.roadsTo[self.counter].traffic_light.cycle_duration

        if self.initial:
            self.roadsTo[self.counter].traffic_light.state = 'green'
            self.initial = False
        if time() - self.time > cycleDuration / con.timeMultiplier:
            self.roadsTo[self.counter].traffic_light.state = 'red'
            self.counter = 0 if self.counter == len(self.roadsTo) - 1 else self.counter + 1
            self.roadsTo[self.counter].traffic_light.state = 'green'
            self.time = time()

    # def addCarWaitTime(self, car):
    #     self.waiting_cars.append(car)
    #     car.stopTimeStart = time() 
    #     avg_wait_time = self.calcAverageStopTime()
        
    # def removeCarWaitTime(self, car):
    #     if car in self.waiting_cars:
    #         car.pauseTime = time() - car.stopTimeStart
    #         self.totalStopTime += car.pauseTime
    #         self.carsPassed += 1
    #         self.waiting_cars.remove(car)

    def calcAverageStopTime(self):
        if self.carsPassed == 0:
            return 0 
        return self.totalStopTime / self.carsPassed 