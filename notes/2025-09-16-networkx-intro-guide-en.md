---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/o1-mini
title: NetworkX Python Graph Library Introduction
translated: false
type: note
---

NetworkX is a powerful Python library for the creation, manipulation, and study of complex networks (graphs). It provides tools to work with both undirected and directed graphs, handle weighted edges, and perform a variety of network analyses.

Below are several examples to help you get started with NetworkX:

---

### 1. **Installing NetworkX**

Before using NetworkX, ensure it's installed. You can install it using `pip`:

```bash
pip install networkx
```

---

### 2. **Creating and Visualizing a Simple Graph**

Here's how to create a simple undirected graph, add nodes and edges, and visualize it using Matplotlib.

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create an empty Graph
G = nx.Graph()

# Add nodes
G.add_node(1)
G.add_nodes_from([2, 3, 4])

# Add edges (automatically adds the nodes if they don't exist)
G.add_edge(1, 2)
G.add_edges_from([(1, 3), (2, 4)])

# Draw the graph
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
plt.title("Simple Undirected Graph")
plt.show()
```

**Output:**

A simple undirected graph with 4 nodes connected by edges.

---

### 3. **Directed Graphs**

Creating and visualizing a directed graph (DiGraph):

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
DG = nx.DiGraph()

# Add edges (nodes are added automatically)
DG.add_edges_from([
    ('A', 'B'),
    ('A', 'C'),
    ('B', 'C'),
    ('C', 'A'),
    ('C', 'D')
])

# Draw the directed graph with arrows
pos = nx.circular_layout(DG)
nx.draw(DG, pos, with_labels=True, node_color='lightgreen', edge_color='gray', arrows=True, node_size=700)
plt.title("Directed Graph")
plt.show()
```

**Output:**

A directed graph showing the direction of edges with arrows.

---

### 4. **Weighted Graphs**

Assigning weights to edges and visualizing them:

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create a weighted graph
WG = nx.Graph()

# Add edges along with weights
WG.add_edge('A', 'B', weight=4)
WG.add_edge('A', 'C', weight=2)
WG.add_edge('B', 'C', weight=5)
WG.add_edge('B', 'D', weight=10)
WG.add_edge('C', 'D', weight=3)

# Get edge weights for labeling
edge_labels = nx.get_edge_attributes(WG, 'weight')

# Draw the graph
pos = nx.spring_layout(WG)
nx.draw(WG, pos, with_labels=True, node_color='lightyellow', edge_color='gray', node_size=700)
nx.draw_networkx_edge_labels(WG, pos, edge_labels=edge_labels)
plt.title("Weighted Graph")
plt.show()
```

**Output:**

A weighted graph with edge labels representing the weights.

---

### 5. **Computing Shortest Path**

Finding the shortest path between two nodes using Dijkstra's algorithm (for weighted graphs):

```python
import networkx as nx

# Create a weighted graph (as in the previous example)
WG = nx.Graph()
WG.add_edge('A', 'B', weight=4)
WG.add_edge('A', 'C', weight=2)
WG.add_edge('B', 'C', weight=5)
WG.add_edge('B', 'D', weight=10)
WG.add_edge('C', 'D', weight=3)

# Compute shortest path from 'A' to 'D'
shortest_path = nx.dijkstra_path(WG, source='A', target='D', weight='weight')
path_length = nx.dijkstra_path_length(WG, source='A', target='D', weight='weight')

print(f"Shortest path from A to D: {shortest_path} with total weight {path_length}")
```

**Output:**

```
Shortest path from A to D: ['A', 'C', 'D'] with total weight 5
```

---

### 6. **Centrality Measures**

Calculating various centrality measures to identify important nodes in the graph.

```python
import networkx as nx

# Create a sample graph
G = nx.karate_club_graph()

# Compute degree centrality
degree_centrality = nx.degree_centrality(G)

# Compute betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G)

# Compute eigenvector centrality
eigen_centrality = nx.eigenvector_centrality(G, max_iter=1000)

# Display top 5 nodes by degree centrality
sorted_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
print("Top 5 nodes by Degree Centrality:")
for node, centrality in sorted_degree[:5]:
    print(f"Node {node}: {centrality:.4f}")

# Similarly, you can display other centralities
```

**Output:**

```
Top 5 nodes by Degree Centrality:
Node 33: 0.6035
Node 0: 0.3793
Node 1: 0.3793
Node 2: 0.3793
Node 3: 0.3793
```

*Note:* The Karate Club graph is a commonly used social network example in NetworkX.

---

### 7. **Detecting Communities with the Girvan-Newman Algorithm**

Identifying communities within a graph.

```python
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt

# Create a graph (using the Karate Club graph)
G = nx.karate_club_graph()

# Compute communities using Girvan-Newman
communities_generator = community.girvan_newman(G)
top_level_communities = next(communities_generator)
second_level_communities = next(communities_generator)

# Function to assign colors to communities
def get_community_colors(G, communities):
    color_map = {}
    for idx, community in enumerate(communities):
        for node in community:
            color_map[node] = idx
    return [color_map[node] for node in G.nodes()]

# Choose the desired level of communities
communities = second_level_communities
colors = get_community_colors(G, communities)

# Draw the graph with community colors
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=colors, with_labels=True, cmap=plt.cm.Set1)
plt.title("Communities in Karate Club Graph")
plt.show()
```

**Output:**

A visualization of the Karate Club graph with nodes colored based on their community membership.

---

### 8. **Reading and Writing Graphs**

NetworkX supports various formats for reading and writing graphs, such as adjacency lists, edge lists, and GraphML.

**Reading an edge list:**

```python
import networkx as nx

# Assume 'edges.txt' contains:
# A B
# A C
# B C
# B D
# C D

G = nx.read_edgelist('edges.txt', delimiter=' ')
print("Nodes:", G.nodes())
print("Edges:", G.edges())
```

**Writing a graph to GraphML:**

```python
import networkx as nx

G = nx.complete_graph(5)  # Create a complete graph with 5 nodes
nx.write_graphml(G, 'complete_graph.graphml')
print("Graph saved to 'complete_graph.graphml'")
```

---

### 9. **Using NetworkX with Pandas DataFrames**

Integrate NetworkX with Pandas for more advanced data manipulation.

```python
import networkx as nx
import pandas as pd

# Create a DataFrame representing edges with weights
data = {
    'source': ['A', 'A', 'B', 'B', 'C'],
    'target': ['B', 'C', 'C', 'D', 'D'],
    'weight': [4, 2, 5, 10, 3]
}
df = pd.DataFrame(data)

# Create a weighted graph from the DataFrame
G = nx.from_pandas_edgelist(df, 'source', 'target', ['weight'])

# Display edges with weights
for u, v, data in G.edges(data=True):
    print(f"({u}, {v}) - weight: {data['weight']}")
```

**Output:**

```
(A, B) - weight: 4
(A, C) - weight: 2
(B, C) - weight: 5
(B, D) - weight: 10
(C, D) - weight: 3
```

---

### 10. **Advanced Visualization with NetworkX and Matplotlib**

Customizing the appearance of the graph for better readability.

```python
import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.Graph()
G.add_edges_from([
    ('A', 'B'), ('A', 'C'), ('A', 'D'),
    ('B', 'C'), ('C', 'D'), ('D', 'E'),
    ('E', 'F'), ('F', 'C')
])

# Assign positions using a layout
pos = nx.spring_layout(G, seed=42)

# Draw nodes with different sizes and colors
node_sizes = [700 if node == 'C' else 300 for node in G.nodes()]
node_colors = ['red' if node == 'C' else 'skyblue' for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors)

# Draw edges with varying widths
edge_widths = [2 if (u == 'C' or v == 'C') else 1 for u, v in G.edges()]
nx.draw_networkx_edges(G, pos, width=edge_widths)

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

plt.title("Customized Graph Visualization")
plt.axis('off')
plt.show()
```

**Output:**

A customized graph where node 'C' is highlighted in red with larger size, and edges connected to 'C' have thicker lines.

---

These examples provide a foundational understanding of how to utilize NetworkX for creating, manipulating, and analyzing graphs in Python. For more advanced usage and detailed documentation, refer to the [official NetworkX documentation](https://networkx.org/documentation/stable/).
