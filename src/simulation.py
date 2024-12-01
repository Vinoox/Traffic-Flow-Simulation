from city_generator import City
import pygame as pg
import config as con
from junction import Junction
from road import Road


#lstOfCars = [car0, car1, car2]

def drawCity(lstOfJunctions: list, lstOfRoads: list, window):
        win_width, win_height = window.get_size()
        margin = 100
        x_coords = [j.x for j in lstOfJunctions]
        y_coords = [j.y for j in lstOfJunctions]
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        def scale_position(pos: tuple):
            x = int((pos[0] - min_x) / (max_x - min_x) * (win_width - 2 * margin) + margin)
            y = int((pos[1] - min_y) / (max_y - min_y) * (win_height - 2 * margin) + margin)
            return (x, y)

        for road in lstOfRoads:
            start = scale_position(road.start)
            end = scale_position(road.end)
            pg.draw.line(window, (0, 255, 0), start, end, 5)

        for junction in lstOfJunctions:
            pg.draw.circle(window, (255, 255, 255), scale_position((junction.x, junction.y)), 20)

        pg.display.flip()

# Inicjalizacja Pygame
def simulation():
    c = City(con.netRows, con.netCols, con.seed)
    lstOfJunctions = [Junction(node) for node in c]
    lstOfRoads = [Road(edge) for edge in c.edges]
    
    pg.init()
    window = pg.display.set_mode((1800, 1000))
    pg.display.set_caption("Graf miasta")
    running = True

    # Pętla główna Pygame
    while running:
        drawCity(lstOfJunctions, lstOfRoads, window)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


    pg.quit()