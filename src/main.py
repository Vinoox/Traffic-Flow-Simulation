import ctypes
import pygame as pg
import config as con
from simulation import simulation


if __name__ == "__main__":
    pg.init()

    window = pg.display.set_mode((0, 0), pg.RESIZABLE)
    HWND = pg.display.get_wm_info()['window']
    SW_MAXIMIZE = 3
    ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)
    con.winWidth, con.winHeight = window.get_size()
    con.winWidth -= 100
    con.winHeight += 100

    pg.display.set_caption("Traffic Flow Simulation")
    clock = pg.time.Clock()
    clock.tick(con.fps)


    #simulation
    city = simulation(window, clock)

    lst = []
    id = []
    for junction in city.junctions:
        id.append(str(junction.id))
        print(f'id: {junction.id}; avg wait time: {junction.calcAverageStopTime()}; total cars passed: {junction.carsPassed}')
        lst.append(junction.calcAverageStopTime())
    print(lst)
    print(id)

    
    pg.quit()