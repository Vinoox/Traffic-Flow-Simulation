from city_generator import City

class Junction():
    def __init__(self, id: tuple, pos: tuple):
        self.id = id
        self.x = pos[0]
        self.y = pos[1]