from city_generator import City
import pygame as pg
import config as con
from car import Car


def drawCity(city: City, window):
    window.fill((0, 0, 0))

    for road in city.roads:
        pg.draw.aaline(window, road.setColor(), road.start, road.end, 0)

    for junction in city.junctions:
        pg.draw.circle(window, (255, 255, 255), (junction.x, junction.y), 10)

    for road in city.roads:
        pg.draw.circle(window, road.traffic_light.get_color(), road.traffic_light.position, 5)

def createCar(city: City):
    car = Car(city)
    print(car.currentNode, car.endNode)
    return car

def drawCar(car: Car, window):
    pg.draw.circle(window, (51, 204, 255), (car.x, car.y), 4)




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
        lstOfCars = prev_state['cars']
    else:
        # Inicjalizacja nowego stanu, jeśli brak poprzedniego
        c = City(con.netRows, con.netCols, con.seed)
        lstOfCars = []

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

        # Aktualizacja świateł na drogach
        for road in c.roads:
            road.update_light()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    lstOfCars.append(createCar(c))  # Generowanie auta
                if event.key == pg.K_ESCAPE:
                    simulation_running = not simulation_running

                if event.key == pg.K_c:
                    lstOfCars.clear()

        if simulation_running:
            lstOfCars.append(createCar(c))

        for car in lstOfCars:
            # Zatrzymywanie samochodu na czerwonym świetle
            car.move(lstOfCars)
            if car.end:
                lstOfCars.remove(car)
            drawCar(car, window)

        drawText(window, f'fps: {clock.get_fps():.1f}', (1700, 40), (255, 255, 255))

        pg.display.flip()
        clock.tick(con.fps)

    pg.quit()


