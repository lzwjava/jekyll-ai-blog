---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Bellman-Ford Algorithm Overview
translated: false
type: note
---

Question: How does the Bellman-Ford algorithm work?

Answer:

The Bellman-Ford algorithm is a single-source shortest path algorithm that computes the shortest distances from a single source vertex to all other vertices in a weighted graph. It works even with negative edge weights and can detect negative cycles.

### Key Features
- Handles negative weights (unlike Dijkstra's algorithm).
- Detects if a negative-weight cycle exists (which would make shortest paths undefined).
- Time complexity: O(V × E), where V is the number of vertices and E is the number of edges.

### How It Works (Step-by-Step)

1. **Initialization**:
   - Set the distance to the source vertex `source` as 0: `dist[source] = 0`.
   - Set the distance to all other vertices as infinity: `dist[v] = ∞` for v ≠ source.
   - Optionally, keep a predecessor array to reconstruct paths.

2. **Relaxation Phase** (repeated V-1 times):
   - For each edge (u, v) with weight w in the graph:
     - If `dist[v] > dist[u] + w`:
       - Update `dist[v] = dist[u] + w`.
       - (Optionally update predecessor[v] = u).
   - This is done exactly |V| - 1 times because the shortest path to any vertex can have at most |V| - 1 edges (in a graph without negative cycles).

   Each iteration ensures that shortest paths with up to k edges are correctly computed.

3. **Negative Cycle Detection**:
   - Perform one additional relaxation pass (the V-th iteration).
   - If any distance can still be improved (i.e., `dist[v] > dist[u] + w` for some edge), then a negative cycle exists reachable from the source.
   - If no updates occur, the distances in `dist[]` are the true shortest paths.

### Pseudocode

```python
def bellman_ford(graph, source):
    dist = {vertex: float('inf') for vertex in graph.vertices}
    dist[source] = 0

    for _ in range(len(graph.vertices) - 1):
        for u, v, w in graph.edges:  # each edge (u → v) with weight w
            if dist[u] != float('inf') and dist[v] > dist[u] + w:
                dist[v] = dist[u] + w

    # Check for negative cycles
    for u, v, w in graph.edges:
        if dist[u] != float('inf') and dist[v] > dist[u] + w:
            raise ValueError("Graph contains a negative-weight cycle")

    return dist
```

### Why It Works
In a graph without negative cycles, the shortest path between any two vertices has at most V-1 edges. By relaxing all edges V-1 times, we guarantee that all shortest paths are found. The extra pass reliably detects if further relaxation is possible due to a negative cycle.

### Example
Consider a graph:
- Vertices: A, B, C
- Edges: A→B (weight 4), A→C (weight 2), C→B (weight -3)

Running Bellman-Ford from A:
- After init: dist[A]=0, dist[B]=∞, dist[C]=∞
- Iteration 1: dist[B]=4, dist[C]=2
- Iteration 2: dist[B]=2 + (-3) = -1 (relax C→B)
- No more changes → shortest distances: A:0, B:-1, C:2

No negative cycle here. If we added B→C with weight -5, a negative cycle would form and be detected.
