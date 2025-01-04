from city_generator import City
import pygame as pg
import config as con
from car import Car
from time import time
def drawCity(city: City, window):
    window.fill((0, 0, 0))

    for road in city.roads:            
        pg.draw.aaline(window, road.setColor(), road.start, road.end, 0)

    for junction in city.junctions:
        pg.draw.circle(window, (255, 255, 255), (junction.x, junction.y), 7)

    for road in city.roads:
        pg.draw.circle(window, road.traffic_light.state, road.traffic_light.position, 5)

def createCar(city: City):
    n = 0
    while n < 100:
        n += 1
        newCar = Car(city)
        if not newCar.road.traffic > newCar.road.maxSize:
            if newCar.road.traffic == 0:
                newCar.road.cars_on_road.append(newCar)
                newCar.road.traffic += 1
                city.totalTraffic += 1
                city.lstOfCars.append(newCar)
                return newCar
            inFront = newCar.road.cars_on_road[-1]
            distance_to_car = ((newCar.x - inFront.x) ** 2 + (newCar.y - inFront.y) ** 2) ** 0.5
            if distance_to_car > 20:
                newCar.road.cars_on_road.append(newCar)
                newCar.road.traffic += 1
                city.totalTraffic += 1
                city.lstOfCars.append(newCar)
                return newCar
# print(car.currentNode, car.endNode)

def drawCar(car: Car, window):
    pg.draw.circle(window, (51, 204, 255), (car.x, car.y), 3)

def isMouseNearRoad(mouse_pos, road, tolerance=3):
    x1, y1 = road.start
    x2, y2 = road.end

    # Oblicz wektor drogi (odcinka)
    dx = x2 - x1
    dy = y2 - y1
    line_length = (dx ** 2 + dy ** 2) ** 0.5

    if line_length == 0:
        return False

    dx /= line_length
    dy /= line_length

    px = mouse_pos[0] - x1
    py = mouse_pos[1] - y1

    projection = px * dx + py * dy

    closest_x = x1 + projection * dx
    closest_y = y1 + projection * dy

    if projection < 0:
        closest_x, closest_y = x1, y1
    elif projection > line_length:
        closest_x, closest_y = x2, y2

    distance = ((closest_x - mouse_pos[0]) ** 2 + (closest_y - mouse_pos[1]) ** 2) ** 0.5

    return distance <= tolerance


def drawText(window, text, position, color=(255, 255, 255)):
    font = pg.font.Font(None, 30)
    label = font.render(text, True, color)
    window.blit(label, position)

def simulation(prev_state=None):
    """
    Funkcja symulacji, która zachowuje poprzednie wartości stanu symulacji.

    Args:
        prev_state (dict): Słownik zawierający poprzednie wartości symulacji,
                           takie jak miasto, lista samochodów itp.
    """
    # Jeśli istnieje poprzedni stan, go wykorzystujemy
    if prev_state:
        c = prev_state['city']
    else:
        # Inicjalizacja nowego stanu, jeśli brak poprzedniego
        c = City(con.netRows, con.netCols, con.seed)

    pg.init()
    window = pg.display.set_mode((con.winWidth, con.winHeight), pg.RESIZABLE)
    pg.display.set_caption("Graf miasta")
    clock = pg.time.Clock()
    running = True
    simulation_running = prev_state['running'] if prev_state else False

    while running:
        clock.tick(con.fps)
        drawCity(c, window)
        mouse_pos = pg.mouse.get_pos()

        #city update
        for road in c.roads:
            c.update(road.id, road.color)

        #light update
        for junction in c.junctions:
            junction.update_light()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    createCar(c)

                #spawnig cars
                if event.key == pg.K_ESCAPE:
                    simulation_running = not simulation_running

                #clear map
                if event.key == pg.K_c:
                    c.lstOfCars.clear()
                    for road in c.roads:
                        road.traffic = 0
                        road.cars_on_road.clear()

                if event.key == pg.K_t:
                    con.timeMultiplier = float(input("set time multipler: "))

                if event.key == pg.K_r:
                    for road in c.roads:
                        road.traffic_light.state = 'red'

                if event.key == pg.K_g:
                    for road in c.roads:
                        road.traffic_light.state = 'green'

                if event.key == pg.K_x:
                    for road in c.roads:
                        print(road.id, road.totalTraffic)

        if simulation_running:
            if c.totalTraffic < 10000:
                createCar(c)

        for car in c.lstOfCars:
            # Zatrzymywanie samochodu na czerwonym świetle
            car.update()
            car.move()
            if car.end:
                c.lstOfCars.remove(car)
            drawCar(car, window)

        drawText(window, f'fps: {clock.get_fps():.1f}', (1700, 40), (255, 255, 255))
        drawText(window, f'cars: {len(c.lstOfCars)}', (1700, 60), (255, 255, 255))

        pg.display.flip()
        clock.tick(con.fps)

    pg.quit()