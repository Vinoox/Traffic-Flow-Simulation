from city_generator import City
import pygame as pg
import threading
import config as con
from car import Car
from road import Road
from junction import Junction
from time import time

def drawCity(city: City, window):
    window.fill((0, 0, 0))
    drawFrame(city, window)

    for road in city.roads:            
        pg.draw.aaline(window, road.getColor(), road.start, road.end, 0)

    for junction in city.junctions:
        pg.draw.circle(window, junction.getColor(), (junction.x, junction.y), 10)

    for road in city.roads:
        pg.draw.circle(window, road.traffic_light.state, road.traffic_light.position, 5)

    for car in city.lstOfCars:
        pg.draw.circle(window, (51, 204, 255), (car.x, car.y), 3)

def drawFrame(city: City, window):
    x = [val[0] for val in city.scalePos.values()]
    y = [val[1] for val in city.scalePos.values()]
    minX, maxX = min(x) - 15, max(x) + 15
    minY, maxY = min(y) - 15, max(y) + 15

    pg.draw.rect(window, (255, 255, 255), (minX, minY, maxX - minX, maxY - minY), 3)

def createCar(city: City, start=None, end=None):
    if city.carsOnRoad < city.capacity // 20:
        n = 0
        while n < 5:
            n += 1
            newCar = Car(city, city.totalTraffic, start, end)
            if newCar.road.traffic < newCar.road.maxSize:
                if newCar.road.traffic == 0:
                    newCar.road.cars_on_road.append(newCar)
                    newCar.road.traffic += 1
                    city.totalTraffic += 1
                    city.lstOfCars.append(newCar)
                    return 0
                inFront = newCar.road.cars_on_road[-1]
                distance_to_car = ((newCar.x - inFront.x) ** 2 + (newCar.y - inFront.y) ** 2) ** 0.5
                if distance_to_car > 10:
                    newCar.road.cars_on_road.append(newCar)
                    newCar.road.traffic += 1
                    city.totalTraffic += 1
                    city.lstOfCars.append(newCar)
                    return 0
        print("No space for car")
    print("City is full")
    return 1
    # print(car.currentNode, car.endNode)

def carSpawner(city: City, stop_event: threading.Event, interval: float):
    while not stop_event.is_set():
        createCar(city)
        stop_event.wait(interval)

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

def isMouseNearJunction(mouse_pos, junction, tolerance=10):
    x, y = junction.pos()
    distance = ((x - mouse_pos[0]) ** 2 + (y - mouse_pos[1]) ** 2) ** 0.5

    return distance <= tolerance

def isMouseNearCar(mouse_pos, car, tolerance=5):
    distance = ((car.x - mouse_pos[0]) ** 2 + (car.y - mouse_pos[1]) ** 2) ** 0.5

    return distance <= tolerance

def checkIfClose(city: City, mouse_pos, window):
    for car in city.lstOfCars:
        if isMouseNearCar(mouse_pos, car):
            drawText(window, f'Car {car.id}', mouse_pos, (0, 0, 255))
            return car

    for junction in city.junctions:
        if isMouseNearJunction(mouse_pos, junction):
            drawText(window, f'Junction {junction.id}', mouse_pos, (0, 0, 255))
            return junction

    for road in city.roads:
        if isMouseNearRoad(mouse_pos, road):
            drawText(window, f'Road {road.id}', mouse_pos, (0, 0, 255))
            return road
    return 0

def drawText(window, text, position, color=(255, 255, 255)):
    font = pg.font.Font(None, 30)
    label = font.render(text, True, color)
    window.blit(label, position)

def highLightRoute(car: Car):
    car.city.getJunction(car.startNode).active = True
    car.city.getJunction(car.endNode).active = True

    for x in range(len(car.path) - 1):
        car.city.getRoad((car.path[x], car.path[x + 1])).active = True


def unHighLight(city: City):
    for junction in city.junctions:
        junction.active = False

    for road in city.roads:
        road.active = False

    for car in city.lstOfCars:
        car.active = False

def simulation(window, clock):
    """
    Funkcja symulacji, która zachowuje poprzednie wartości stanu symulacji.

    Args:
        prev_state (dict): Słownik zawierający poprzednie wartości symulacji,
                           takie jak miasto, lista samochodów itp.
    """
    # # Jeśli istnieje poprzedni stan, go wykorzystujemy
    # if prev_state:
    #     c = prev_state['city']
    # else:
    #     # Inicjalizacja nowego stanu, jeśli brak poprzedniego
    #     c = City(con.netRows, con.netCols, con.seed)

    c = City(con.netRows, con.netCols, con.seed)
    print(f'City capacity: {c.capacity}')
    window = window
    stop_event = threading.Event()
    clock = clock
    running = True
    activeSpawning = False
    simulationRunning = True
    carThread = None

    while running:
        drawCity(c, window)
        mouse_pos = pg.mouse.get_pos()
        events = pg.event.get()

        checkIfClose(c, mouse_pos, window)

        for event in events:
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if simulationRunning:
                        simulationRunning = not simulationRunning
                        stop_event.set()
                        if carThread is not None:
                            carThread.join()
                            carThread = None
                    else:
                        simulationRunning = not simulationRunning
                        stop_event.clear()
                        stop_event = threading.Event()
                        if activeSpawning:
                            carThread = threading.Thread(target=carSpawner, args=(c, stop_event, 0.05 / con.timeMultiplier), daemon=True)
                            carThread.start()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    object = checkIfClose(c, mouse_pos, window)
                    if type(object) == Car:
                        unHighLight(c)
                        object.active = True
                        highLightRoute(object)
                    else:
                        unHighLight(c)


############################
        if simulationRunning:
            #city update
            for road in c.roads:
                c.update(road.id, road.trafficColor)

            #light update
            for junction in c.junctions:
                junction.update_light()

            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_t:
                        con.timeMultiplier = float(input("set time multipler: "))
                        if activeSpawning:
                            stop_event.set()
                            carThread.join()

                            stop_event.clear()
                            carThread = threading.Thread(target=carSpawner, args=(c, stop_event, 0.05 / con.timeMultiplier), daemon=True)
                            carThread.start()


                    if event.key == pg.K_TAB:
                        createCar(c)

                    #spawnig cars
                    if event.key == pg.K_ESCAPE:
                        if not activeSpawning:
                            activeSpawning = True
                            stop_event.clear()
                            stop_event = threading.Event()
                            carThread = threading.Thread(target=carSpawner, args=(c, stop_event, 0.05 / con.timeMultiplier), daemon=True)
                            carThread.start()
                        else:
                            activeSpawning = False
                            stop_event.set()
                            carThread.join()
                            carThread = None

                    #clear map
                    if event.key == pg.K_c:
                        c.lstOfCars.clear()
                        for road in c.roads:
                            road.traffic = 0
                            road.cars_on_road.clear()

                    if event.key == pg.K_r:
                        for road in c.roads:
                            road.traffic_light.state = 'red'

                    if event.key == pg.K_g:
                        for road in c.roads:
                            road.traffic_light.state = 'green'

                    if event.key == pg.K_x:
                        for road in c.roads:
                            print(road.id, road.totalTraffic)

            for car in c.lstOfCars:
                # Zatrzymywanie samochodu na czerwonym świetle
                car.update()
                car.move()
                if car.end:
                    if car.active: unHighLight(c)
                    c.lstOfCars.remove(car)
                

        drawText(window, f'fps: {clock.get_fps():.1f}', (1700, 40), (255, 255, 255))
        drawText(window, f'cars: {len(c.lstOfCars)}', (1700, 60), (255, 255, 255))
        drawText(window, f'Sim running: {simulationRunning}', (1700, 80), (255, 255, 255))
        drawText(window, f'Car spawning: {activeSpawning}', (1700, 100), (255, 255, 255))

        pg.display.flip()
        clock.tick(con.fps)