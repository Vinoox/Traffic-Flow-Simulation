import networkx as nx
import config as con
import matplotlib.pyplot as plt
from junction import Junction
from road import Road
import random

class City:
    def __init__(self, rows: int, cols: int, seed=None):
        self.rows = rows
        self.cols = cols
        self.seed = seed
        self.lstOfCars = []
        self.carsOnRoad = 0
        self.totalTraffic = 0
        self.capacity = 0
        random.seed(self.seed)  # Ustawienie seeda

        # generowanie modelu miasta
        self.G = nx.grid_2d_graph(rows, cols)
        self.pos = self.randomize_node_positions()
        self.add_edge_weights()

        # generowanie przeskalowanych pozycji do wyświetlania
        self.scalePos = self.generate_scale_position()
        self.scaleEdges = self.generate_edges_positions()

        x = [val[0] for val in self.scalePos.values()]
        y = [val[1] for val in self.scalePos.values()]
        self.minX, self.maxX = min(x) - 15, max(x) + 15
        self.minY, self.maxY = min(y) - 15, max(y) + 15

        # generowanie skrzyżowań i dróg
        self.junctions = [Junction(id, pos) for id, pos in self.scalePos.items()]
        self.roads = [Road(key, val) for key, val in self.scaleEdges.items()]
        for road in self.roads:
            self.capacity += road.maxSize

            for junction in self.junctions:
                if road.id[0] == junction.id:
                    junction.roadsFrom.append(road)
                if road.id[1] == junction.id:
                    junction.roadsTo.append(road)


    def getRoad(self, id: tuple):
        for road in self.roads:
            if id == road.id:
                return road
            
    def getJunction(self, id: tuple):
        for junction in self.junctions:
            if id == junction.id:
                return junction

    def scale(self, pos: tuple):
        self.X = [val[0] for val in self.pos.values()]
        self.Y = [val[1] for val in self.pos.values()]
        self.minX, self.maxX = min(self.X), max(self.X)
        self.minY, self.maxY = min(self.Y), max(self.Y)

        x = (pos[0] - self.minX) / (self.maxX - self.minX)
        y = (pos[1] - self.minY) / (self.maxY - self.minY)

        x_pixel = int(x * (con.winWidth - 2 * con.margin) + con.margin / 2)
        y_pixel = int((1 - y) * (con.winHeight - 2 * con.margin) + con.margin/4)  # Odwrócenie Y

        return x_pixel, y_pixel

    def generate_scale_position(self):
        scalePos = {}
        for key, val in self.pos.items():
            scalePos[key] = self.scale(val)
        return scalePos

    def generate_edges_positions(self):
        edges = {}
        for edge in self.G.edges():
            startId, endId = edge[0], edge[1]
            start, end = self.scalePos[edge[0]], self.scalePos[edge[1]]

            dx, dy = end[0] - start[0], end[1] - start[1]

            length = (dx ** 2 + dy ** 2) ** 0.5

            offset = 3

            perp_dx, perp_dy = -dy / length * offset, dx / length * offset

            start1 = (int(start[0] + perp_dx), int(start[1] + perp_dy))
            end1 = (int(end[0] + perp_dx), int(end[1] + perp_dy))
            start2 = (int(start[0] - perp_dx), int(start[1] - perp_dy))
            end2 = (int(end[0] - perp_dx), int(end[1] - perp_dy))

            edges[(startId, endId)] = ((start1, end1))
            edges[(endId, startId)] = ((end2, start2))
        return edges

    def randomize_node_positions(self):
        return {(x, y): (y + random.uniform(-0.4, 0.4), -x + random.uniform(-0.4, 0.4))
                for x, y in self.G.nodes()}

    def add_edge_weights(self):
        for u, v in self.G.edges():
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            self.G[u][v]['weight'] = distance

    def update(self, id, color):
        self.carsOnRoad = len(self.lstOfCars)
        x1, y1 = id[0]
        x2, y2 = id[1]
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if color == 'green': self.G[id[0]][id[1]]['weight'] = distance
        elif color == 'orange': self.G[id[0]][id[1]]['weight'] = distance * 2
        else: self.G[id[0]][id[1]]['weight'] = distance * 3

    def find_shortest_path(self, source, target):
        shortest_path = nx.dijkstra_path(self.G, source=source, target=target, weight='weight')
        return shortest_path

    def draw(self, shortest_path=None):
        plt.figure(figsize=(8, 8))

        nx.draw(
            self.G,
            self.pos,
            with_labels=True,
            node_color="lightblue",
            edge_color="black",
            arrows=True,
            node_size=800,
            font_size=10,
        )

        if shortest_path:
            path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
            nx.draw_networkx_edges(self.G, self.pos, edgelist=path_edges, edge_color="red", width=2)

        plt.show()