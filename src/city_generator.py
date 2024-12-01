import networkx as nx
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

        self.G = nx.grid_2d_graph(rows, cols)  # Graf nieskierowany
        self.pos = self.generate_node_positions()  # Pozycje węzłów
        self.edges = self.generate_edges_positions()
        self.add_edge_weights()  # Dodawanie wag na podstawie odległości euklidesowej

    def __iter__(self):
        for node, nodePos in self.pos.items():
            yield (nodePos)

    def generate_edges_positions(self):
        edges = []
        for edge in self.G.edges():
            node1, node2 = edge[0], edge[1]
            edges.append((self.pos[node1], self.pos[node2]))
        return edges

    def generate_node_positions(self):
        """
        Generowanie losowych pozycji dla każdego węzła w grafie.
        Pozycje są losowane wokół siatki.
        """
        return {(x, y): (y + random.uniform(-0.5, 0.5), -x + random.uniform(-0.5, 0.5)) 
                for x, y in self.G.nodes()}

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
        path_length = nx.shortest_path_length(self.G, source=source, target=target, weight='weight')
        return shortest_path, path_length

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