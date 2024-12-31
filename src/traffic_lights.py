color = {'red': (255, 0, 0),
         'green': (0, 255, 0),
         'orange': (221, 244, 7)}

import numpy as np

class TrafficLight:
    def __init__(self, pos: tuple, vector: tuple):
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
        self.state = 'red'  # 'green' lub 'red'
        self.cycle_duration = 5
        self.timer = 0  # Licznik do zmiany świateł