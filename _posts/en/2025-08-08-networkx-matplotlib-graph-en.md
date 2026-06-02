---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: NetworkX and Matplotlib Graph Tutorial
translated: false
type: note
---

### Installing the Libraries

To use NetworkX and Matplotlib for drawing diagrams, install them if needed:

- NetworkX: Handles graph creation and manipulation.
- Matplotlib: Provides plotting capabilities.

Install via pip:

```bash
pip install networkx matplotlib
```

For faster rendering, Matplotlib recommends installing NumPy (`pip install numpy`).

### Basic Setup and Example

1. **Import libraries**:

   ```python
   import networkx as nx
   import matplotlib.pyplot as plt
   ```

2. **Create a graph**:
   Use NetworkX to build a simple undirected graph (you can customize with directed graphs, weighted edges, etc.):

   ```python
   G = nx.Graph()  # Create an empty graph
   G.add_nodes_from([1, 2, 3, 4, 5])  # Add nodes (e.g., 5 nodes)
   G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])  # Add edges (connections)
   ```

3. **Draw and display the diagram**:
   Use Matplotlib's backend for visualization:

   ```python
   nx.draw(G, with_labels=True)  # Draw the graph with node labels
   plt.show()  # Display the plot
   ```

This produces a basic circular layout of the graph (a cycle with 5 nodes).

### Advanced Customizations

- **Layouts**: Control node positions (e.g., random, spring layout):

  ```python
  pos = nx.spring_layout(G)  # Force-directed layout for realistic networks
  nx.draw(G, pos=pos, with_labels=True, node_color='lightblue', edge_color='gray')
  plt.title("Network Diagram")
  plt.show()
  ```

- **Node and edge styles**: Customize appearance:

  ```python
  nx.draw(G, pos=pos, node_size=500, node_color='red', edge_width=2, font_size=10)
  ```

- **Directed graphs**: For hierarchical relationships, use `nx.DiGraph`.

  ```python
  DG = nx.DiGraph()
  DG.add_edges_from([('A', 'B'), ('B', 'C')])
  nx.draw(DG, with_labels=True, arrows=True)
  plt.show()
  ```

- **Saving the diagram**: Export to file instead of displaying:

  ```python
  plt.savefig('diagram.png')
  ```

### Tips and Resources

- NetworkX docs (networkx.org) for graph types like trees or grids.
- Matplotlib docs (matplotlib.org) for embedding in GUIs or subplots.
- For large graphs (>100 nodes), use `nx.draw_networkx` or external tools like Graphviz for better performance.
- Experiment in a Jupyter notebook for interactive plotting. If issues arise, common errors stem from missing backends (install via `pip install pyqt5` or similar for interactive windows).
