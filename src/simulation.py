from city_generator import City
import pygame as pg
import config as con
from junction import Junction
from road import Road
from car import Car

def drawCity(lstOfJunctions: list[Junction], lstOfRoads: list[Road], window):
    window.fill((0, 0, 0))
    for road in lstOfRoads:
        pg.draw.line(window, road.color, road.start, road.end, 2)

    for junction in lstOfJunctions:
        pg.draw.circle(window, (255, 255, 255), (junction.x, junction.y), 10)

def createCar(city: City):
    car = Car(city)
    print(car.currentNode, car.targetNode)
    return car

def drawCar(car: Car, window):
    pg.draw.circle(window, (255, 255, 255), (car.x, car.y), 5)

# Inicjalizacja Pygame
def simulation():
    c = City(con.netRows, con.netCols, con.seed)
    lstOfJunctions = [Junction(node[0], node[1]) for node in c]
    lstOfRoads = [Road(key, val) for key, val in c.scalEdges.items()]
    lstOfCars = []

    pg.init()
    window = pg.display.set_mode((con.winWidth, con.winHeight), pg.RESIZABLE)
    pg.display.set_caption("Graf miasta")
    clock = pg.time.Clock()
    running = True

    # Pętla główna Pygame
    while running:
        lstOfCars.append(createCar(c))
        drawCity(lstOfJunctions, lstOfRoads, window)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    lstOfCars.append(createCar(c))

        for car in lstOfCars:
            car.move(c)
            drawCar(car, window)

        pg.display.flip()
        clock.tick(con.fps)

    pg.quit()