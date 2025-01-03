color = {'red': (255, 0, 0),
         'green': (0, 255, 0),
         'orange': (221, 244, 7)}

from traffic_light import TrafficLight

class Road:
    def __init__(self, id: tuple, pos: tuple):
        self.id = id
        self.start = pos[0]  # (x, y)
        self.end = pos[1]    # (x, y)
        self.traffic = 0
        self.vector = self.getVector()
        self.maxSize = self.lenght() // 3 + 1
        self.color = 'green'

        self.cars_on_road = []

        # Tworzenie światła na podstawie pozycji drogi
        self.traffic_light = TrafficLight(self.end, self.vector)

    def setColor(self):
        if self.traffic < self.maxSize * 0.1: self.color = 'green' ; return color['green']
        if self.traffic < self.maxSize * 0.2: self.color = 'orange'; return color['orange']
        self.color = 'red'; return color['red']

        #
        # if self.traffic * 3 >= self.lenght() - 6: self.isFull = True; print("Road is full")
        # else: self.isFull = False
        #
    
    def lenght(self):
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]
    
        length = (dx**2 + dy**2)**0.5

        return length

    def update_light(self):
        """
        Aktualizuje stan sygnalizacji świetlnej na drodze.
        """
        if self.traffic_light:
            self.traffic_light.update()

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