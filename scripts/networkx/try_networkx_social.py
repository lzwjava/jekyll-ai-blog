import networkx as nx
import matplotlib.pyplot as plt

# Create a social network graph
social = nx.Graph()

# Add people and their connections
people = ["Alice", "Bob", "Charlie", "David", "Eve"]
social.add_nodes_from(people)

connections = [
    ("Alice", "Bob"),
    ("Alice", "Charlie"),
    ("Bob", "Charlie"),
    ("Bob", "David"),
    ("Charlie", "Eve"),
    ("David", "Eve"),
]
social.add_edges_from(connections)

# Calculate centrality measures
degree_centrality = nx.degree_centrality(social)
betweenness_centrality = nx.betweenness_centrality(social)
closeness_centrality = nx.closeness_centrality(social)

print("Degree Centrality:", degree_centrality)
print("Betweenness Centrality:", betweenness_centrality)
print("Closeness Centrality:", closeness_centrality)

# Visualize
nx.draw(social, with_labels=True, node_color="lightgreen", node_size=2000)
plt.show()
