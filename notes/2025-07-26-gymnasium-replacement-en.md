---
audio: false
generated: true
lang: en
layout: post
title: 'Gymnasium: The Modern Gym for RL'
translated: false
type: note
---

The Gym library refers to a popular Python toolkit originally developed by OpenAI for reinforcement learning (RL), a subfield of machine learning where agents learn to make decisions by interacting with environments to maximize rewards. It provides a standardized API and a collection of benchmark environments (like games, robotics simulations, and classic control problems) to develop, test, and compare RL algorithms. This makes it easier for researchers and developers to prototype without building environments from scratch.

Key features include:
- **Environments**: Pre-built tasks such as CartPole (balancing a pole), Atari games, or MuJoCo physics simulations.
- **API Simplicity**: You create an environment with `gym.make("EnvironmentName")`, then use methods like `reset()` to start, `step(action)` to interact and get observations/rewards, and `render()` to visualize.
- **Extensibility**: Users can create custom environments by subclassing Gym's base classes.
- **Integration**: Works well with libraries like Stable Baselines, RLlib, or PyTorch/TensorFlow for implementing RL agents.

However, the original OpenAI Gym is no longer actively maintained and has been deprecated since around 2021. It's recommended to use **Gymnasium**, which is a direct fork and continuation by the Farama Foundation. Gymnasium is fully compatible (you can import it as `import gymnasium as gym`), adds improvements like better vectorized environments for parallel training, stricter type checking, and ongoing updates. Installation is via `pip install gymnasium`, with extras like `pip install gymnasium[atari]` for specific environments.

Example basic usage in Python:
```python
import gymnasium as gym

env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset(seed=42)

for _ in range(1000):
    action = env.action_space.sample()  # Random action (agent would learn better ones)
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
```

If you're starting with RL, Gymnasium is the go-to choice today for most projects.

[OpenAI Gym GitHub](https://github.com/openai/gym)
[Gymnasium Documentation](https://gymnasium.farama.org/)
[Gym Documentation (Legacy)](https://www.gymlibrary.dev/)
