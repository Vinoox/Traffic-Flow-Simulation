import numpy as np

class TrafficLight:
    def __init__(self, pos: tuple, vector: tuple, initial_state='green', cycle_duration=300):
        """
        Tworzy obiekt świateł drogowych.

        :param start_pos: Początkowa pozycja drogi (x, y).
        :param end_pos: Końcowa pozycja drogi (x, y).
        :param offset: Odległość przesunięcia świateł od węzła (teraz możemy to pominąć).
        :param initial_state: Początkowy stan ('green' lub 'red').
        :param cycle_duration: Długość cyklu świateł w klatkach.
        """
        # Ustalanie pozycji świateł na środku drogi
        self.position = tuple(np.subtract(pos, np.multiply(vector, 12)))
        self.state = initial_state  # 'green' lub 'red'
        self.cycle_duration = cycle_duration
        self.timer = 0  # Licznik do zmiany świateł

    def update(self):
        """
        Aktualizuje stan świateł na podstawie licznika czasu.
        """
        self.timer += 1
        if self.timer >= self.cycle_duration:
            self.state = 'red' if self.state == 'green' else 'green'
            self.timer = 0

    def get_color(self):
        """
        Zwraca kolor świateł w formacie RGB.
        """
        if self.state == 'green':
            return (0, 255, 0)  # Zielony
        return (255, 0, 0)  # Czerwony