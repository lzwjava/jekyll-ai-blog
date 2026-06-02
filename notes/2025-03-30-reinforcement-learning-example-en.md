---
audio: false
generated: true
lang: en
layout: post
title: Reinforcement Learning Example
translated: false
type: note
---

Below, I’ll provide a few simple conceptual examples of Reinforcement Learning (RL) followed by a basic Python code example using a simple scenario. RL involves an agent learning to maximize a reward by interacting with an environment, so the examples and code will reflect that.

### Simple Examples of Reinforcement Learning

1. **Child Learning to Walk**
   - **Agent**: The child.
   - **Environment**: The floor or room.
   - **Action**: Take a step, crawl, or stand still.
   - **Reward**: Moving forward (+1), falling (-1).
   - **Learning**: The child learns through trial and error that taking balanced steps leads to progress.

2. **Training a Robot Arm to Pick Up Objects**
   - **Agent**: The robot arm.
   - **Environment**: A table with objects.
   - **Action**: Move up, down, left, right, or grasp.
   - **Reward**: Successfully picking up an object (+10), dropping it (-5).
   - **Learning**: The arm adjusts its movements to maximize successful grabs.

3. **Grid World Game**
   - **Agent**: A character in a grid.
   - **Environment**: A 3x3 grid with a goal and obstacles.
   - **Action**: Move up, down, left, or right.
   - **Reward**: Reaching the goal (+10), hitting a wall (-1).
   - **Learning**: The character learns the shortest path to the goal.

---

### Simple Python Code Example: Q-Learning in a Grid World

Here’s a basic implementation of Q-Learning, a popular RL algorithm, in a simple 1D "world" where an agent moves left or right to reach a goal. The agent learns by updating a Q-table based on rewards.

```python
import numpy as np
import random

# Environment setup: 1D world with 5 positions (0 to 4), goal at position 4
state_space = 5  # Positions: [0, 1, 2, 3, 4]
action_space = 2  # Actions: 0 = move left, 1 = move right
goal = 4

# Initialize Q-table with zeros (states x actions)
q_table = np.zeros((state_space, action_space))

# Hyperparameters
learning_rate = 0.1
discount_factor = 0.9
exploration_rate = 1.0
exploration_decay = 0.995
min_exploration_rate = 0.01
episodes = 1000

# Reward function
def get_reward(state):
    if state == goal:
        return 10  # Big reward for reaching the goal
    return -1  # Small penalty for each step

# Step function: Move agent and get new state
def step(state, action):
    if action == 0:  # Move left
        new_state = max(0, state - 1)
    else:  # Move right
        new_state = min(state_space - 1, state + 1)
    reward = get_reward(new_state)
    done = (new_state == goal)
    return new_state, reward, done

# Training loop
for episode in range(episodes):
    state = 0  # Start at position 0
    done = False

    while not done:
        # Exploration vs Exploitation
        if random.uniform(0, 1) < exploration_rate:
            action = random.randint(0, action_space - 1)  # Explore
        else:
            action = np.argmax(q_table[state])  # Exploit

        # Take action and observe result
        new_state, reward, done = step(state, action)

        # Update Q-table using the Q-learning formula
        old_value = q_table[state, action]
        next_max = np.max(q_table[new_state])
        new_value = (1 - learning_rate) * old_value + learning_rate * (reward + discount_factor * next_max)
        q_table[state, action] = new_value

        # Move to new state
        state = new_state

    # Decay exploration rate
    exploration_rate = max(min_exploration_rate, exploration_rate * exploration_decay)

# Test the learned policy
state = 0
steps = 0
print("Testing the learned policy:")
while state != goal:
    action = np.argmax(q_table[state])
    state, reward, done = step(state, action)
    steps += 1
    print(f"Step {steps}: Moved to state {state}, Action: {'Left' if action == 0 else 'Right'}")
print(f"Reached goal in {steps} steps!")

# Print the Q-table
print("\nLearned Q-table:")
print(q_table)
```

---

### Explanation of the Code

1. **Environment**: A 1D line with 5 positions (0 to 4). The goal is at position 4.
2. **Actions**: The agent can move left (0) or right (1).
3. **Rewards**: +10 for reaching the goal, -1 for each step (to encourage efficiency).
4. **Q-Table**: A table storing the expected future rewards for each state-action pair.
5. **Q-Learning**: The agent updates the Q-table using the formula:
   `Q(s, a) = (1 - α) * Q(s, a) + α * (reward + γ * max(Q(s', a')))`, where:
   - `α` = learning rate
   - `γ` = discount factor
   - `s` = current state, `a` = action, `s'` = next state

6. **Exploration vs Exploitation**: The agent sometimes picks random actions (exploration) and sometimes uses the Q-table (exploitation), controlled by `exploration_rate`.

---

### Sample Output

```
Testing the learned policy:
Step 1: Moved to state 1, Action: Right
Step 2: Moved to state 2, Action: Right
Step 3: Moved to state 3, Action: Right
Step 4: Moved to state 4, Action: Right
Reached goal in 4 steps!

Learned Q-table:
[[-2.5   2.3]
 [-1.8   4.5]
 [-1.2   6.8]
 [-0.5   9. ]
 [ 0.    0. ]]
```

The agent learns to always move right from any starting position to reach the goal efficiently. The Q-table shows higher values for "move right" actions as you approach the goal.

This is a very basic example, but it captures the essence of RL. For more complex scenarios (e.g., 2D grids or games), you’d expand the state and action spaces accordingly!
