---
audio: false
generated: true
lang: en
layout: post
title: Monte Carlo Tree Search
translated: false
type: note
---

Let’s dive into a comprehensive guide on **Monte Carlo Tree Search (MCTS)**, a powerful algorithm widely used in decision-making problems, especially in games and artificial intelligence. I’ll break it down step-by-step, covering its origins, core concepts, mechanics, implementation, strengths, weaknesses, and applications—everything you need to grasp it thoroughly.

---

### What is Monte Carlo Tree Search?

Monte Carlo Tree Search is a heuristic search algorithm that combines the precision of tree search with the randomness of Monte Carlo methods. It’s particularly effective for problems with large, complex decision spaces where exhaustively exploring all possibilities (like in minimax) isn’t feasible. MCTS builds a partial search tree incrementally, using random simulations to guide its exploration toward promising moves.

- **Origins**: MCTS emerged in the mid-2000s, with significant contributions from Rémi Coulom (2006) and others. It gained fame when it powered Go-playing AI, notably in AlphaGo, revolutionizing how computers tackle games with vast state spaces.
- **Key Use Case**: Games like Go, Chess, Poker, and even real-world problems like planning or optimization.

---

### Core Concepts

MCTS operates on a **tree** where:
- **Nodes** represent game states or decision points.
- **Edges** represent actions or moves leading to new states.
- The **root** is the current state from which decisions are made.

The algorithm balances **exploration** (trying new moves) and **exploitation** (focusing on known good moves) using a statistical approach. It doesn’t require a perfect evaluation function—just a way to simulate outcomes.

---

### The Four Phases of MCTS

MCTS iterates through four distinct steps in each simulation cycle:

#### 1. **Selection**
- Start at the root and traverse the tree to a leaf node (a node not fully expanded or a terminal state).
- Use a **selection policy** to choose child nodes. The most common is the **Upper Confidence Bound applied to Trees (UCT)** formula:
  \\[
  UCT = \bar{X}_i + C \sqrt{\frac{\ln(N)}{n_i}}
  \\]
  - \\(\bar{X}_i\\): Average reward (win rate) of the node.
  - \\(n_i\\): Number of visits to the node.
  - \\(N\\): Number of visits to the parent node.
  - \\(C\\): Exploration constant (typically \\(\sqrt{2}\\) or tuned per problem).
- UCT balances exploitation (\\(\bar{X}_i\\)) and exploration (the \\(\sqrt{\frac{\ln(N)}{n_i}}\\) term).

#### 2. **Expansion**
- If the selected leaf node isn’t terminal and has unvisited children, expand it by adding one or more child nodes (representing untried moves).
- Typically, only one child is added per iteration to control memory usage.

#### 3. **Simulation (Rollout)**
- From the newly expanded node, run a **random simulation** (or rollout) to a terminal state (e.g., win/loss/draw).
- The simulation uses a lightweight policy—often uniform random moves—since evaluating every state precisely is too costly.
- The outcome (e.g., +1 for a win, 0 for a draw, -1 for a loss) is recorded.

#### 4. **Backpropagation**
- Propagate the simulation result back up the tree, updating statistics for each visited node:
  - Increment the visit count (\\(n_i\\)).
  - Update the total reward (e.g., sum of wins or average win rate).
- This refines the tree’s knowledge about which paths are promising.

Repeat these steps for many iterations (e.g., thousands), then pick the best move from the root based on the most visited child or highest average reward.

---

### How MCTS Works: An Example

Imagine a simple tic-tac-toe game:
1. **Root**: Current board state (e.g., X’s turn with a partially filled board).
2. **Selection**: UCT picks a promising move (e.g., placing X in the center) based on prior simulations.
3. **Expansion**: Add a child node for an untried move (e.g., O’s response in a corner).
4. **Simulation**: Play random moves until the game ends (e.g., X wins).
5. **Backpropagation**: Update stats—center move gets +1 reward, visit count increases.

After thousands of iterations, the tree reveals that placing X in the center has a high win rate, so it’s chosen.

---

### Pseudocode

Here’s a basic MCTS implementation:

```python
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0

def mcts(root, iterations):
    for _ in range(iterations):
        node = selection(root)
        if not node.state.is_terminal():
            node = expansion(node)
        reward = simulation(node.state)
        backpropagation(node, reward)
    return best_child(root)

def selection(node):
    while node.children and not node.state.is_terminal():
        node = max(node.children, key=uct)
    return node

def expansion(node):
    untried_moves = node.state.get_untried_moves()
    if untried_moves:
        move = random.choice(untried_moves)
        new_state = node.state.apply_move(move)
        child = Node(new_state, parent=node)
        node.children.append(child)
        return child
    return node

def simulation(state):
    current = state.clone()
    while not current.is_terminal():
        move = random.choice(current.get_moves())
        current.apply_move(move)
    return current.get_result()

def backpropagation(node, reward):
    while node:
        node.visits += 1
        node.reward += reward
        node = node.parent

def uct(child):
    if child.visits == 0:
        return float('inf')  # Explore unvisited nodes
    return (child.reward / child.visits) + 1.41 * math.sqrt(math.log(child.parent.visits) / child.visits)

def best_child(node):
    return max(node.children, key=lambda c: c.visits)  # Or use reward/visits
```

---

### Strengths of MCTS

1. **Anytime Algorithm**: Stop it anytime and get a reasonable move based on current stats.
2. **No Evaluation Function Needed**: Relies on simulations, not domain-specific heuristics.
3. **Scalable**: Works in huge state spaces (e.g., Go with \\(10^{170}\\) possible positions).
4. **Adaptive**: Naturally focuses on promising branches as iterations increase.

---

### Weaknesses of MCTS

1. **Computationally Intensive**: Requires many simulations for good results, which can be slow without optimization.
2. **Shallow Exploration**: May miss deep strategies if iterations are limited.
3. **Randomness Dependency**: Poor rollout policies can skew results; quality depends on simulation accuracy.
4. **Memory Usage**: Tree growth can be a bottleneck in memory-constrained environments.

---

### Enhancements and Variations

To address weaknesses, MCTS is often enhanced:
- **Heuristics in Rollouts**: Use domain knowledge (e.g., preferring center moves in tic-tac-toe) instead of pure randomness.
- **Parallelization**: Run multiple simulations concurrently (root parallelization or tree parallelization).
- **RAVE (Rapid Action Value Estimation)**: Share statistics across similar moves to speed convergence.
- **Integration with Neural Networks**: As in AlphaGo, use neural nets to guide selection (policy network) and evaluate states (value network).

---

### Applications

1. **Games**:
   - Go (AlphaGo’s breakthrough).
   - Chess (combined with neural networks in engines like Leela Chess Zero).
   - Poker (handles imperfect information with adaptations).
2. **Robotics**: Path planning in uncertain environments.
3. **Optimization**: Solving combinatorial problems like scheduling or resource allocation.
4. **Real-Time Strategy**: Decision-making in dynamic, unpredictable scenarios.

---

### Practical Tips for Implementation

- **Tune \\(C\\)**: Adjust the UCT exploration constant based on your problem (\\(C = \sqrt{2}\\) is a starting point).
- **Limit Tree Growth**: Prune nodes or cap expansion to manage memory.
- **Optimize Rollouts**: Use lightweight simulations or heuristics to save time.
- **Test Iterations**: Experiment with 100, 1,000, or 10,000 iterations to balance speed and quality.

---

### Conclusion

MCTS is a versatile, elegant algorithm that shines in domains where traditional search methods falter. Its beauty lies in its simplicity—random simulations guided by a growing tree—yet it scales to tackle some of the hardest problems in AI. Whether you’re coding a game AI or solving a planning task, MCTS offers a robust starting point, especially when paired with modern enhancements like neural networks.

If you’d like, I can walk you through a specific implementation (e.g., for tic-tac-toe) or explore a particular aspect—like UCT tuning or parallel MCTS—in more detail. What do you think?
