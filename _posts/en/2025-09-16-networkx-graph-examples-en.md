---
audio: false
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: NetworkX Graph Creation and Analysis Examples
translated: false
type: note
---

NetworkX is a powerful Python library for creating, analyzing, and visualizing complex networks. Here are several examples demonstrating its capabilities:

## 1. Basic Graph Creation and Visualization

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create an empty graph
G = nx.Graph()

# Add nodes
G.add_node(1)
G.add_nodes_from([2, 3])
G.add_nodes_from(range(4, 7))

# Add edges
G.add_edge(1, 2)
G.add_edges_from([(2, 3), (3, 4), (4, 5), (5, 6), (6, 1)])

# Visualize the graph
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray')
plt.show()
```

## 2. Directed Graph Example

```python
# Create a directed graph
D = nx.DiGraph()

# Add edges (automatically adds nodes)
D.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)])

# Draw with different node colors
pos = nx.spring_layout(D)
nx.draw(D, pos, with_labels=True, node_color='lightgreen',
        edge_color='red', node_size=1000, arrowsize=20)
plt.show()
```

## 3. Graph Analysis Example

```python
# Create a graph
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5)])

# Basic graph properties
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())
print("Nodes:", G.nodes())
print("Edges:", G.edges())
print("Degree of node 2:", G.degree(2))
print("Neighbors of node 2:", list(G.neighbors(2)))
print("Is graph connected?", nx.is_connected(G))
print("Shortest path from 1 to 5:", nx.shortest_path(G, 1, 5))
```

## 4. Weighted Graph Example

```python
# Create a weighted graph
G = nx.Graph()

# Add weighted edges
G.add_edge('A', 'B', weight=4)
G.add_edge('B', 'C', weight=2)
G.add_edge('A', 'C', weight=1)
G.add_edge('C', 'D', weight=5)

# Draw with edge labels showing weights
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightcoral')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
```

## 5. Social Network Analysis Example

```python
# Create a social network graph
social = nx.Graph()

# Add people and their connections
people = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
social.add_nodes_from(people)

connections = [('Alice', 'Bob'), ('Alice', 'Charlie'),
               ('Bob', 'Charlie'), ('Bob', 'David'),
               ('Charlie', 'Eve'), ('David', 'Eve')]
social.add_edges_from(connections)

# Calculate centrality measures
degree_centrality = nx.degree_centrality(social)
betweenness_centrality = nx.betweenness_centrality(social)
closeness_centrality = nx.closeness_centrality(social)

print("Degree Centrality:", degree_centrality)
print("Betweenness Centrality:", betweenness_centrality)
print("Closeness Centrality:", closeness_centrality)

# Visualize
nx.draw(social, with_labels=True, node_color='lightgreen', node_size=2000)
plt.show()
```

## 6. Random Graph Generation

```python
# Create an Erdős–Rényi random graph
random_graph = nx.erdos_renyi_graph(10, 0.3)  # 10 nodes, 30% edge probability

# Visualize
nx.draw(random_graph, with_labels=True, node_color='skyblue')
plt.show()
```

## 7. Graph Algorithms Example

```python
# Create a graph
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 6), (5, 6)])

# Find all simple paths between two nodes
print("All paths from 1 to 6:", list(nx.all_simple_paths(G, 1, 6)))

# Minimum spanning tree
T = nx.minimum_spanning_tree(G)
print("Edges in MST:", T.edges())

# Community detection (requires python-louvain package)
# pip install python-louvain
try:
    import community as community_louvain
    partition = community_louvain.best_partition(G)
    print("Community partition:", partition)
except ImportError:
    print("Install python-louvain for community detection")
```

These examples cover basic graph creation, visualization, analysis, and some common algorithms. NetworkX provides many more features for working with complex networks.
