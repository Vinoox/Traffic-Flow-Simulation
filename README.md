# Politechnika Wrocławska - Inżyniera Systemów - Symulacja Komputerowa
## **Temat:** Symulacja przepływu ruchu drogowego


ogolnie projekt zostal oceniony na 5.5 ale jest tam sporo do poprawy jezeli chodzi o optymalizacje i naprawe licznych bugow
nie bylo czasu na napisanie zadnego interfejsu wiec sporo rzeczy robi sie przyciskami z klawiatury albo zmienia w kodzie (np. seed)
do tego robilismy kilka eksperymentow i sprawdzalismy jak zastosowanie 'inteligetnych' swiatel wplywa na poprawe przeplywu ruchu
z tego co pamietam do tych badan byl napisany jakis skrypt ktory zliczal potrzebne wartosci i potem robil jakies wykresy ale chyba go ostatecznie wyjebalem wiec to trzeba dopisac xdd

pozdro z fartem

sterowanie symulacja(fragment kodu z pliku simulation.py odpowiedni przycisk wykonuja odpowiadajace im funkcje):
\/
\/
\/
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


---
Joanna Rogalska, Maciej Styś
