color = {'red': (255, 0, 0),
         'green': (0, 255, 0),
         'orange': (221, 244, 7)}

import numpy as np
import config as con

class TrafficLight:
    def __init__(self, pos: tuple, vector: tuple, duration: int):
        self.position = tuple(np.subtract(pos, np.multiply(vector, 12)))
        self.state = 'red'  # 'green' lub 'red'
        self.cycle_duration = duration

    # def updateLight(self, time):
    #     self.cycle_duration = time / con.timeMultiplier