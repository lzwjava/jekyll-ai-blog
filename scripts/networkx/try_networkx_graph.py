import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
D = nx.DiGraph()

# Add edges (automatically adds nodes)
D.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)])

# Draw with different node colors
pos = nx.spring_layout(D)
nx.draw(
    D,
    pos,
    with_labels=True,
    node_color="lightgreen",
    edge_color="red",
    node_size=1000,
    arrowsize=20,
)
plt.show()
