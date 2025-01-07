import threading
from city_generator import City

class Task:
    def __init__(self, city: City, fun, interval: float):
        self.interval = interval
        self.fun = fun
        self.city = city

    def run(self):
        while not self.stopEvent.is_set():
            self.fun(self.city)
            self.stopEvent.wait(self.interval)

    def start(self):
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def stop(self):
        self.stopEvent.set()
        self.thread.join()