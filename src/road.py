color = {'red': (255, 0, 0), 
         'green': (0, 255, 0), 
         'orange': (221, 244, 7)}

class Road():
    def __init__(self, id: tuple, pos: tuple):
        self.id = id
        self.start = pos[0] #(x, y)
        self.end = pos[1]   #(x, y)
        self.traffic = 0

    def setColor(self):
        if self.traffic < 3: return 'green'
        if self.traffic < 5: return 'orange'
        return 'red'
    
    def getVector(self):
        """
        Oblicza znormalizowany wektor ruchu od start do end.
        """
        # Oblicz różnice współrzędnych
        dx = self.end[0] - self.start[0]
        dy = self.end[1] - self.start[1]

        # Oblicz długość wektora
        length = (dx**2 + dy**2)**0.5

        # Normalizacja wektora (jeśli długość > 0)
        if length > 0:
            dx /= length
            dy /= length

        return dx, dy