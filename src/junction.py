class Junction():
    def __init__(self, id: tuple, pos: tuple):
        self.id = id
        self.x = pos[0]
        self.y = pos[1]

    def pos(self):
        return self.x, self.y