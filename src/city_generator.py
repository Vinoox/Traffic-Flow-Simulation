import networkx as nx
import config as con
import matplotlib.pyplot as plt
import random

class City:
    def __init__(self, rows: int, cols: int, seed=None):
        """
        Inicjalizacja miasta: tworzenie grafu 2D o zadanej liczbie wierszy i kolumn
        oraz generowanie pozycji dla węzłów.
        """
        self.rows = rows
        self.cols = cols
        self.seed = seed  # Seed do kontrolowania losowości
        random.seed(self.seed)  # Ustawienie seeda

        #generowanie modelu miasta
        self.G = nx.grid_2d_graph(rows, cols) 
        self.pos = self.randomize_node_positions()  # Pozycje węzłów
        
        self.scalePos = self.generate_scale_position()
        self.scalEdges = self.generate_edges_positions()

        for id, val in self.scalEdges.items():
            print(id, val)

        self.add_edge_weights()  # Dodawanie wag na podstawie odległości euklidesowej

    def __iter__(self):
        for id, Pos in self.scalePos.items():
            yield (id, Pos)

    def generate_edges_positions(self):
        edges = {}
        for edge in self.G.edges():
            startId, endId = edge[0], edge[1]
            start, end = self.scalePos[edge[0]], self.scalePos[edge[1]]
            
            # Obliczanie wektora drogi
            dx, dy = end[0] - start[0], end[1] - start[1]
            
            # Obliczanie wektora prostopadłego i normalizacja
            length = (dx**2 + dy**2) ** 0.5

            offset = 3  # Przesunięcie linii w pikselach

            perp_dx, perp_dy = -dy / length * offset, dx / length * offset
            
            # Przesunięte punkty
            start1 = (int(start[0] + perp_dx), int(start[1] + perp_dy))
            end1 = (int(end[0] + perp_dx), int(end[1] + perp_dy))
            start2 = (int(start[0] - perp_dx), int(start[1] - perp_dy))
            end2 = (int(end[0] - perp_dx), int(end[1] - perp_dy))

            edges[(startId, endId)] = ((start1, end1))
            edges[(endId, startId)] = ((start2, end2))
        return edges

    def randomize_node_positions(self):
        """
        Generowanie losowych pozycji dla każdego węzła w grafie.
        Pozycje są losowane wokół siatki.
        """
        return {(x, y): (y + random.uniform(-0.4, 0.4), -x + random.uniform(-0.4, 0.4)) 
                for x, y in self.G.nodes()}

    def scale(self, pos: tuple):
        self.X = [val[0] for val in self.pos.values()]
        self.Y = [val[1] for val in self.pos.values()]
        self.minX, self.maxX = min(self.X), max(self.X)
        self.minY, self.maxY = min(self.Y), max(self.Y)

        x = int((pos[0] - self.minX) / (self.maxX - self.minX) * (con.winWidth - 2 * con.margin) + con.margin)
        y = int((pos[1] - self.minY) / (self.maxY - self.minY) * (con.winHeight - 2 * con.margin) + con.margin)
        return (x, y)
    
    def generate_scale_position(self):
        scalePos ={}
        for key, val in self.pos.items():
            scalePos[key] = self.scale(val)
        return scalePos

    def add_edge_weights(self):
        """
        Dodawanie wag na podstawie odległości euklidesowej między węzłami.
        """
        for u, v in self.G.edges():
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5  # Odległość euklidesowa
            self.G[u][v]['weight'] = distance

    def find_shortest_path(self, source, target):
        """
        Znajdowanie najkrótszej ścieżki w grafie z uwzględnieniem wag (algorytm Dijkstry).
        """
        shortest_path = nx.shortest_path(self.G, source=source, target=target, weight='weight')
        #path_length = nx.shortest_path_length(self.G, source=source, target=target, weight='weight')
        return shortest_path

    def draw(self, shortest_path=None):
        """
        Rysowanie grafu z możliwością wyróżnienia najkrótszej ścieżki.
        """
        plt.figure(figsize=(8, 8))
        
        # Rysowanie grafu
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

        # Jeśli podano, wyróżnienie najkrótszej ścieżki na grafie
        if shortest_path:
            path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
            nx.draw_networkx_edges(self.G, self.pos, edgelist=path_edges, edge_color="red", width=2)

        plt.show()