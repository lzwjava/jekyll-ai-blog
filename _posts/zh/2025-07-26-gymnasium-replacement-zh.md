---
audio: false
generated: true
lang: zh
layout: post
title: Gymnasium：现代强化学习训练场
translated: true
type: note
---

Gym 库指的是一个流行的 Python 工具包，最初由 OpenAI 开发，用于强化学习（RL）——这是机器学习的一个子领域，智能体通过与环境交互来学习决策，以最大化奖励。它提供了标准化的 API 和一系列基准环境（如游戏、机器人仿真和经典控制问题），用于开发、测试和比较 RL 算法。这使得研究人员和开发者能够更轻松地进行原型设计，而无需从头构建环境。

主要特性包括：

- **环境**：预构建的任务，如 CartPole（平衡杆）、Atari 游戏或 MuJoCo 物理仿真。
- **API 简洁性**：使用 `gym.make("环境名称")` 创建环境，然后使用 `reset()` 方法开始，`step(action)` 进行交互并获取观察结果/奖励，以及 `render()` 进行可视化。
- **可扩展性**：用户可以通过继承 Gym 的基类来创建自定义环境。
- **集成性**：与 Stable Baselines、RLlib 或 PyTorch/TensorFlow 等库良好配合，用于实现 RL 智能体。

然而，原始的 OpenAI Gym 已不再积极维护，并在 2021 年左右被弃用。建议使用 **Gymnasium**，这是由 Farama Foundation 直接分叉并持续维护的版本。Gymnasium 完全兼容（你可以通过 `import gymnasium as gym` 导入），并增加了改进，如更好的向量化环境以支持并行训练、更严格的类型检查以及持续的更新。安装方式为 `pip install gymnasium`，对于特定环境，可以使用附加选项如 `pip install gymnasium[atari]`。

Python 中的基本用法示例：

```python
import gymnasium as gym

env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset(seed=42)

for _ in range(1000):
    action = env.action_space.sample()  # 随机动作（智能体会学习更好的动作）
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

env.close()
```

如果你刚开始学习 RL，Gymnasium 是当前大多数项目的首选。

[OpenAI Gym GitHub](https://github.com/openai/gym)
[Gymnasium 文档](https://gymnasium.farama.org/)
[Gym 文档（旧版）](https://www.gymlibrary.dev/)
