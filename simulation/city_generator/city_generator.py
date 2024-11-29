import networkx as nx
import matplotlib.pyplot as plt
import random

class City:
    def __init__(self, rows, cols, seed=None):
        """
        Inicjalizacja miasta: tworzenie grafu 2D o zadanej liczbie wierszy i kolumn
        oraz generowanie pozycji dla węzłów.
        """
        self.rows = rows
        self.cols = cols
        self.seed = seed  # Seed do kontrolowania losowości
        random.seed(self.seed)  # Ustawienie seeda

        self.G = nx.grid_2d_graph(rows, cols)  # Graf nie-skierowany
        self.pos = self.generate_node_positions()  # Pozycje węzłów
        self.add_edge_weights()  # Dodawanie wag na podstawie odległości euklidesowej

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

# # Tworzenie instancji miasta z seed
# seed_value = 42
# city = City(rows=5, cols=5, seed=seed_value)

# # Znajdowanie najkrótszej ścieżki między (0, 0) a (4, 4)
# shortest_path, path_length = city.find_shortest_path(source=(0, 0), target=(4, 4))

# # Wyświetlenie wyników
# print("Najkrótsza ścieżka (z uwzględnieniem wag):", shortest_path)
# print("Długość najkrótszej ścieżki:", path_length)

# # Rysowanie grafu z wyróżnieniem najkrótszej ścieżki
# city.draw(shortest_path=shortest_path)