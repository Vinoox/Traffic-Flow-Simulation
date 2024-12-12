class Junction():
    def __init__(self, id: tuple, pos: tuple):
        self.id = id
        self.x = pos[0]
        self.y = pos[1]
        self.light_state = 'green'  # Początkowy stan świateł: zielony
        self.light_timer = 0  # Licznik czasu dla zmiany świateł

    def pos(self):
        return self.x, self.y

    def update_light(self):
        self.light_timer += 1
        if self.light_timer > 300:  # Zmień światło co 300 klatek
            self.light_state = 'red' if self.light_state == 'green' else 'green'
            self.light_timer = 0