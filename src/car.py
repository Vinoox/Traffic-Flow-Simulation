from time import time
from junction import Junction
from city_generator import City

class Car():
    def __init__(self, startNode: Junction, targetNode: Junction, city: City):
        self.currentNode = startNode
        self.targetNode = targetNode

        self.x = startNode.x
        self.y = startNode.y
        self.startTime = time()
        self.endTime = 0
        self.path = city.find_shortest_path(self.currentNode, self.targetNode)