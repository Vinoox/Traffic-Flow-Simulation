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
        """
        Ustawia kolor drogi na podstawie gęstości ruchu.
        """
        if self.traffic < 3:
            return 'green'
        if self.traffic < 5:
            return 'orange'
        return 'red'

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