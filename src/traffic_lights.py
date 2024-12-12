class TrafficLight:
    def __init__(self, start_pos, end_pos, offset=20, initial_state='green', cycle_duration=300):
        """
        Tworzy obiekt świateł drogowych.

        :param start_pos: Początkowa pozycja drogi (x, y).
        :param end_pos: Końcowa pozycja drogi (x, y).
        :param offset: Odległość przesunięcia świateł od węzła (teraz możemy to pominąć).
        :param initial_state: Początkowy stan ('green' lub 'red').
        :param cycle_duration: Długość cyklu świateł w klatkach.
        """
        # Ustalanie pozycji świateł na środku drogi
        self.position = self.get_midpoint(start_pos, end_pos)
        self.state = initial_state  # 'green' lub 'red'
        self.cycle_duration = cycle_duration
        self.timer = 0  # Licznik do zmiany świateł

    def get_midpoint(self, start_pos, end_pos, offset_factor=0.8):
        """
        Oblicza środek drogi (pozycję świateł), ale z możliwością przesunięcia go bliżej końca drogi.
        offset_factor: współczynnik, który określa, jak daleko od początku drogi mają być światła (0.5 to środek, 0.8 to bliżej końca).
        """
        x1, y1 = start_pos
        x2, y2 = end_pos

        # Obliczamy przesunięcie wzdłuż wektora drogi
        offset_x = (x2 - x1) * offset_factor
        offset_y = (y2 - y1) * offset_factor

        # Nowe współrzędne światła
        mid_x = x1 + offset_x
        mid_y = y1 + offset_y

        return (mid_x, mid_y)

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