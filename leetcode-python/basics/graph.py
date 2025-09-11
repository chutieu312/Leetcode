import networkx as nx
import matplotlib.pyplot as plt

# --- Adjacency List ---
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0, 3],
    3: [1, 2]
}

# --- Adjacency Matrix ---
adj_matrix = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
]

def plot_adj_list(graph):
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    nx.draw(G, with_labels=True, node_color='lightblue')
    plt.title("Adjacency List Graph")

def plot_adj_matrix(matrix):
    G = nx.Graph()
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                G.add_edge(i, j)
    nx.draw(G, with_labels=True, node_color='lightgreen')
    plt.title("Adjacency Matrix Graph")

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plot_adj_list(graph)
plt.subplot(1, 2, 2)
plot_adj_matrix(adj_matrix)
plt.tight_layout()
plt.show()