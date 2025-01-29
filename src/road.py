color = {'red': (255, 0, 0),
         'green': (0, 255, 0),
         'orange': (221, 244, 7),
         'blue': (0, 0, 255)}

from traffic_light import TrafficLight

class Road:
    def __init__(self, id: tuple, pos: tuple):
        self.id = id
        self.start = pos[0]  # (x, y)
        self.end = pos[1]    # (x, y)
        self.traffic = 0
        self.totalTraffic = 0
        self.normalizedCount = 0
        self.vector = self.getVector()
        self.maxSize = self.lenght() // 3
        self.trafficColor = 'green'
        self.cars_on_road = []
        self.traffic_light = TrafficLight(self.end, self.vector, self.maxSize // 4)

        self.active = False

    def getColor(self):
        if self.active: return color['blue']
        else: return color[self.trafficColor]

    def setColor(self): 
        if self.traffic < self.maxSize * 0.1: 
            self.trafficColor = 'green'
        elif self.traffic < self.maxSize * 0.2: 
            self.trafficColor = 'orange'
        else: 
            self.trafficColor = 'red'

        return  0
    
    def lenght(self):
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
    
        length = (dx**2 + dy**2)**0.5

        return length

    def getVector(self):
        """
        Oblicza znormalizowany wektor ruchu od start do end.
        """
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
        length = (dx ** 2 + dy ** 2) ** 0.5

        if length > 0:
            dx /= length
            dy /= length

        return dx, dy
    
    def isSpace(self):
        if self.traffic == 0: return True
        else:
            distance_to_last_car = ((self.cars_on_road[-1].x - self.start[0]) ** 2 + (self.cars_on_road[-1].y - self.start[1]) ** 2) ** 0.5
            if distance_to_last_car > 5: return True
        return False