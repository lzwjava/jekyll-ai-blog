---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Understanding Dijkstra's Shortest Path Algorithm
translated: false
type: note
---

### Understanding Dijkstra's Shortest Path Algorithm

Dijkstra's algorithm is a fundamental way to find the shortest path between nodes in a graph where edges have non-negative weights (like distances or costs). It's named after Edsger W. Dijkstra and is widely used in GPS navigation, network routing, and more. The key intuition: it explores the graph greedily, always picking the closest unvisited node and updating paths from there, like a ripple effect from the starting point.

#### Quick Prerequisites
- **Graph Basics**: Think of a graph as a map of cities (nodes) connected by roads (edges) with lengths (weights). We assume weights are positive—no negative distances!
- **Directed vs. Undirected**: Works for both, but examples here use undirected for simplicity.
- **Shortest Path**: The path with the minimal total weight from source to target.

If graphs are new, imagine a social network: people (nodes), friendships with "strength" scores (weights).

#### How It Works: Step-by-Step Intuition
Dijkstra builds the shortest path incrementally, using a **priority queue** (like a to-do list sorted by urgency—here, by current shortest known distance). It never revisits nodes once settled, making it efficient.

1. **Initialize**:
   - Pick a starting node (source). Set its distance to 0.
   - Set all other nodes' distances to infinity (∞).
   - Track the "path to" each node (initially none).

2. **While there are unvisited nodes**:
   - Pick the unvisited node with the smallest current distance (from the priority queue).
   - "Settle" it: Mark it as visited. This distance is final—thanks to non-negative weights, no shorter path can be found later.
   - For each neighbor of this node:
     - Calculate potential new distance: (settled node's distance) + (edge weight to neighbor).
     - If this is shorter than the neighbor's current distance, update it and note the path came via the settled node.
   - Repeat until all nodes are visited or the target is settled.

The algorithm stops early if you only care about one target node.

**Why it works**: It's like breadth-first search but weighted—always expanding the cheapest frontier first. Proof relies on the fact that once a node is settled, its distance can't improve (greedy choice property).

#### Simple Example
Imagine a graph with 4 cities: A (start), B, C, D. Edges and weights:

- A → B: 4
- A → C: 2
- B → C: 1
- B → D: 5
- C → D: 8

ASCII visualization:
```
   4
A ----- B
 \     / \
  2   1   5
  \   /     |
   C ------- D
     8
```

Run Dijkstra from A:

- **Start**: dist[A]=0, dist[B]=∞, dist[C]=∞, dist[D]=∞. Queue: A.
- **Settle A** (dist=0).
  - Update B: 0+4=4
  - Update C: 0+2=2
  - Queue: C(2), B(4)
- **Settle C** (dist=2).
  - Update D: 2+8=10
  - Queue: B(4), D(10)
- **Settle B** (dist=4).
  - Update C: 4+1=5 (but 2<5, no change)
  - Update D: 4+5=9 (9<10, update to 9)
  - Queue: D(9)
- **Settle D** (dist=9).

Final distances: A=0, B=4, C=2, D=9.
Path to D: A → B → D (total 9, shorter than A → C → D=10).

You can trace back paths using a "previous node" array.

#### Pseudocode
Here's a simple implementation outline (Python-like):

```python
import heapq  # For priority queue

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    pq = [(0, start)]  # (distance, node)

    while pq:
        current_dist, current = heapq.heappop(pq)
        if current_dist > distances[current]:
            continue  # Outdated entry

        for neighbor, weight in graph[current].items():
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct path to target (e.g., 'D')
    path = []
    node = 'D'
    while node is not None:
        path.append(node)
        node = previous[node]
    return path[::-1], distances['D']  # Reverse to get start-to-end
```

- `graph`: Dict of dicts, e.g., `{'A': {'B':4, 'C':2}, ...}`
- Time Complexity: O((V+E) log V) with a binary heap (V=vertices, E=edges). Great for sparse graphs.

#### Tips to Grasp It Deeper
- **Visualize**: Draw your graph on paper, simulate steps with a table of distances/visited.
- **Common Pitfalls**: Fails with negative weights (use Bellman-Ford instead). Assumes connected graph.
- **Practice**: Try on small graphs, then code it for a map dataset.
- **Variants**: A* adds heuristics for faster searches (e.g., in games).

This should click—start with the example, run it mentally a few times!

[Wikipedia: Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
[GeeksforGeeks: Visual Explanation](https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/)
