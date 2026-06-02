---
audio: false
generated: true
lang: en
layout: post
title: A* (A-star) Search Algorithm
translated: false
type: note
---

The **A* (A-star) search algorithm** is a popular pathfinding and graph traversal algorithm used in computer science and artificial intelligence. It is widely used for finding the shortest path from a starting point (or node) to a target (or goal) in a graph, while efficiently exploring possible paths.

A*combines elements of **Dijkstra's Algorithm** (which guarantees the shortest path) and **Greedy Best-First Search** (which tries to find the goal as quickly as possible). The key feature of A* is that it uses both the actual cost to reach a node (from the start node) and a heuristic that estimates the cost from that node to the goal.

### How A* Works

1. **Start with an open list**: The open list contains nodes that are yet to be explored. Initially, only the start node is on this list.
2. **Calculate scores**: Each node in the open list is assigned a score based on two factors:
   - **g(n)**: The cost to reach the current node from the start node.
   - **h(n)**: A heuristic estimate of the cost to reach the goal from the current node (this is domain-specific, like straight-line distance or Euclidean distance).
   - **f(n) = g(n) + h(n)**: The total estimated cost, used to prioritize nodes. Nodes with the lowest f(n) are explored first.
3. **Expand the most promising node**: The node with the lowest f(n) score is chosen for exploration. It is moved to a "closed list" of nodes already explored.
4. **Check neighbors**: The algorithm examines the neighbors of the current node. If a neighbor hasn’t been visited or can be reached with a lower cost, it is added to the open list.
5. **Repeat** until the goal is reached or the open list is empty (indicating no path exists).

### Key Components

- **g(n)**: The actual cost from the start node to the current node.
- **h(n)**: The heuristic estimate from the current node to the goal (can vary depending on the problem).
- **f(n) = g(n) + h(n)**: The total cost that prioritizes nodes for exploration.

### Heuristics

The heuristic function is critical for A*’s efficiency. A common heuristic for grid-based pathfinding is the **Manhattan distance** (sum of horizontal and vertical distances) or **Euclidean distance** (straight-line distance) for continuous spaces.

### Example Use Cases

- **Navigation systems** (GPS)
- **Games and AI** (pathfinding for characters or agents)
- **Robotics** (for planning efficient paths)

In summary, A* is a highly efficient algorithm because it systematically explores paths based on both the known cost and estimated future cost, ensuring that it finds the optimal solution when possible.
