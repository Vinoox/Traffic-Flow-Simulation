from time import time
import config as con

class Junction():
    def __init__(self, id: tuple, pos: tuple):
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.roadsFrom = []
        self.roadsTo = []
        self.time = time()
        self.initial = True
        self.counter = 0

    def pos(self):
        return self.x, self.y

    def update_light(self):
        if self.initial:
            self.roadsTo[self.counter].traffic_light.state = 'green'
            self.initial = False
        if time() - self.time > self.roadsTo[self.counter].traffic_light.cycle_duration / con.timeMultiplier:
            self.roadsTo[self.counter].traffic_light.state = 'red'
            self.counter = 0 if self.counter == len(self.roadsTo) - 1 else self.counter + 1
            self.roadsTo[self.counter].traffic_light.state = 'green'
            self.time = time()