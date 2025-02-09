from city_generator import City
import pygame as pg
import config as con
from car import Car
from junction import Junction
from background_task import Task
from time import time


def drawCity(city: City, window):
    window.fill((0, 0, 0))
    drawFrame(city, window)

    for road in city.roads:
        pg.draw.aaline(window, road.getColor(), road.start, road.end, 0)

    for junction in city.junctions:
        pg.draw.circle(window, junction.getColor(), (junction.x, junction.y), 10)
        if junction.start: drawText(window, 'S', (junction.pos()[0] - 5, junction.pos()[1] - 5), (0, 0, 0), 20)
        if junction.end: drawText(window, 'E', (junction.pos()[0] - 5, junction.pos()[1] - 5), (0, 0, 0), 20)

    for road in city.roads:
        pg.draw.circle(window, road.traffic_light.state, road.traffic_light.position, 5)

    for car in city.lstOfCars:
        pg.draw.circle(window, (0, 0, 0), (car.x, car.y), car.getSize())
        pg.draw.circle(window, car.getColor(), (car.x, car.y), car.getSize() - 1)
        if car.active:
            drawText(window, f'Car: {car.id} time: {car.existTime:.2f}', (con.winWidth - 100, 160), (255, 255, 255))
            drawText(window, f'Stop time: {car.totalWaitTime:.2f}', (con.winWidth - 100, 180), (255, 255, 255))

def drawFrame(city: City, window):
    pg.draw.rect(window, (255, 255, 255), (city.minX, city.minY, city.maxX - city.minX, city.maxY - city.minY), 3)

def createCar(city: City, start=None, end=None, amountOfCars = 1000):
    if city.totalTraffic < amountOfCars:
        n = 0
        while True:
            n += 1
            newCar = Car(city, city.totalTraffic, start, end)
            if newCar.road.traffic < newCar.road.maxSize:
                if newCar.road.traffic == 0:
                    newCar.road.cars_on_road.append(newCar)
                    newCar.road.traffic += 1
                    city.totalTraffic += 1
                    city.lstOfCars.append(newCar)
                    return newCar
                inFront = newCar.road.cars_on_road[-1]
                distance_to_car = ((newCar.x - inFront.x) ** 2 + (newCar.y - inFront.y) ** 2) ** 0.5
                if distance_to_car > 10:
                    newCar.road.cars_on_road.append(newCar)
                    newCar.road.traffic += 1
                    city.totalTraffic += 1
                    city.lstOfCars.append(newCar)
                    return newCar
        print("No space for car")
        return 1
    # print("City is full")
    return 1

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
            avg_stop_time = junction.calcAverageStopTime()
            drawText(window, f'Junction {junction.id}', mouse_pos, (0, 0, 255))
            drawText(window, f'Avg Wait: {avg_stop_time:.2f}s',(mouse_pos[0], mouse_pos[1] + 15),
                     (0, 0, 255), 30)
            return junction

    for road in city.roads:
        if isMouseNearRoad(mouse_pos, road):
            drawText(window, f'Road {road.id}', mouse_pos, (0, 0, 255))
            return road
    return 0

def drawText(window, text, position, color=(255, 255, 255), size=30):
    font = pg.font.Font(None, size)
    label = font.render(text, True, color)
    window.blit(label, position)

def highLightRoute(car: Car):
    car.active = True
    startJunction = car.city.getJunction(car.startNode)
    startJunction.start = True

    endJunction = car.city.getJunction(car.endNode)
    endJunction.end = True

    for x in range(len(car.passRoute) - 1):
        car.city.getRoad((car.passRoute[x], car.passRoute[x + 1])).active = True

    for x in range(len(car.path) - 1):
        car.city.getRoad((car.path[x], car.path[x + 1])).active = True

def unHighLight(city: City):
    for junction in city.junctions:
        junction.start = False
        junction.end = False

    for road in city.roads:
        road.active = False

    for car in city.lstOfCars:
        car.active = False

def carsUpdate(city: City):
    for car in city.lstOfCars:
        car.update()
        car.move()
        if car.active and car.updatedPath:
            unHighLight(city)
            highLightRoute(car)

        if car.end:
            if car.active: unHighLight(city)
            city.lstOfCars.remove(car)

def cityUpdate(city: City):
    for road in city.roads:
        road.setColor()
        city.update(road.id, road.trafficColor)

    # light update
    for junction in city.junctions:
        junction.update_light()

def simulation(window, clock):
    c = City(con.netRows, con.netCols, con.seed)



    window = window
    simulator = Task(c, carsUpdate, 0.005)
    cityUp = Task(c, cityUpdate, 0.5 / con.timeMultiplier)

    carSpawner = Task(c, createCar, 0.01 / con.timeMultiplier)
    clock = clock
    running = True
    activeSpawning = False
    simulationRunning = True
    stopTime = 0
    simulator.start()
    cityUp.start()
    startTime = time()

    while running:
        drawCity(c, window)
        mouse_pos = pg.mouse.get_pos()
        events = pg.event.get()
        checkIfClose(c, mouse_pos, window)

        for event in events:
            if event.type == pg.QUIT:
                running = False
                return c

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if simulationRunning:
                        simulationRunning = not simulationRunning
                        stopTime = time()
                        if activeSpawning: carSpawner.stop()
                        simulator.stop()
                        cityUp.stop()

                    else:
                        simulationRunning = not simulationRunning
                        for car in c.lstOfCars:
                            car.stopTimeUpdate(time() - stopTime)
                      
                        simulator.start()
                        cityUp.start()
                        if activeSpawning: carSpawner.start()

                if event.key == pg.K_ESCAPE:
                    if not activeSpawning:
                        activeSpawning = True
                        if simulationRunning:
                            carSpawner.start()
                    else:
                        activeSpawning = False
                        carSpawner.stop()

                if event.key == pg.K_BACKSPACE:
                    running = False
                    return c

                if event.key == pg.K_t:
                    con.timeMultiplier = float(input("set time multipler: "))
                    if activeSpawning:
                        carSpawner.stop()
                        carSpawner.start()

                if event.key == pg.K_TAB:
                    unHighLight(c)
                    car = createCar(c)
                    if car != 1: highLightRoute(car)

                if event.key == pg.K_c:
                    c.lstOfCars.clear()
                    unHighLight(c)
                    for road in c.roads:
                        road.traffic = 0
                        road.cars_on_road.clear()

                if event.key == pg.K_r:
                    for road in c.roads:
                        road.traffic_light.state = 'red'

                if event.key == pg.K_a:
                    for junction in c.junctions:
                        junction.active = not junction.active

                if event.key == pg.K_g:
                    for road in c.roads:
                        road.traffic_light.state = 'green'

                if event.key == pg.K_x:
                    for road in c.roads:
                        print(road.id, road.totalTraffic)

                if event.key == pg.K_1:
                    con.timeMultiplier = 1

                if event.key == pg.K_2:
                    con.timeMultiplier = 2

                if event.key == pg.K_3:
                    con.timeMultiplier = 3

                if event.key == pg.K_4:
                    con.timeMultiplier = 4

                if event.key == pg.K_5:
                    con.timeMultiplier = 5

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    object = checkIfClose(c, mouse_pos, window)
                    if type(object) == Car:
                        unHighLight(c)
                        highLightRoute(object)
                    elif type(object) == Junction:
                        object.active = not object.active
                    else:
                        unHighLight(c)

        # drawText(window, f'time: {time() - startTime:.2f}', (con.winWidth - 105, 40), (255, 255, 255))
        drawText(window, f'fps: {clock.get_fps():.1f}', (con.winWidth - 105, 60), (255, 255, 255))
        drawText(window, f'cars: {len(c.lstOfCars)}', (con.winWidth - 105, 80), (255, 255, 255))
        drawText(window, f'Sim running: {simulationRunning}', (con.winWidth - 105, 100), (255, 255, 255))
        drawText(window, f'Car spawning: {activeSpawning}', (con.winWidth - 105, 120), (255, 255, 255))
        drawText(window, f'Time multiplier: x{con.timeMultiplier}', (con.winWidth - 105, 140), (255, 255, 255))

        clock.tick(con.fps)
        pg.display.flip()