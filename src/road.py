from city_generator import City

class Road():
    def __init__(self, pos: tuple):
        self.start = pos[0]
        self.end = pos[1]