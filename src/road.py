color = {'red': (255, 0, 0),
         'green': (0, 255, 0),
         'orange': (221, 244, 7)}

from traffic_lights import TrafficLight
class Road:
    def __init__(self, id: tuple, pos: tuple):
        self.id = id
        self.start = pos[0]  # (x, y)
        self.end = pos[1]    # (x, y)
        self.traffic = 0
        self.vector = self.getVector()

        self.cars_on_road = []

        # Tworzenie światła na podstawie pozycji drogi
        self.traffic_light = TrafficLight(self.end, self.vector)

    def setColor(self):
        if self.traffic * 4 < self.lenght() * 0.1: return color['green']
        if self.traffic * 4 < self.lenght() * 0.3: return color['orange']
        return color['red']
    
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