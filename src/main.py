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
    pg.display.set_caption("Traffic Flow Simulation")
    clock = pg.time.Clock()
    clock.tick(con.fps)


    #start window
    
    city = simulation(window, clock)
    
    #end window
    
    
    pg.quit()