from city_generator import City
import random

colorr = [(255, 0, 0), (0, 255, 0), (221, 244, 7)]

class Road():
    def __init__(self, id: tuple, pos: tuple):
        self.id = id
        self.start = pos[0]
        self.end = pos[1]
        self.color = (random.choice(colorr))
        self.counter = 0