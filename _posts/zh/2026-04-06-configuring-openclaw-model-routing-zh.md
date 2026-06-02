---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 配置OpenClaw模型路由
translated: true
type: note
---

问题：如何在 OpenClaw 中设置默认模型为 `openrouter/minimax/minimax-m2.7` 并切换到本地 `DeepSeek R1`？

答案：

你正在配置 **OpenClaw 模型路由**。这包含两部分：

* 设置 **默认模型** → `openrouter/minimax/minimax-m2.7`
* **手动**切换到本地模型 → `/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf`

以下是正确的操作方法。

---

# 方法 1 — 设置默认模型（推荐）

编辑你的 **OpenClaw 配置文件**：

```
~/.openclaw/config.yaml
```

或项目级别的配置文件：

```
.openclaw/config.yaml
```

设置：

```yaml
model: openrouter/minimax/minimax-m2.7
```

现在 OpenClaw 将 **默认使用 MiniMax M2.7**。

---

# 方法 2 — 交互式切换模型

在 OpenClaw 聊天界面内输入：

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

这将立即切换到 **本地 DeepSeek R1**。

切换回：

```
/model openrouter/minimax/minimax-m2.7
```

---

# 方法 3 — 命令行启动覆盖

你也可以这样启动 OpenClaw：

```
openclaw --model openrouter/minimax/minimax-m2.7
```

或使用本地模型：

```
openclaw --model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

---

# 方法 4 — 工作区级别（按项目）

在项目根目录创建：

```
.project-root/.openclaw/config.yaml
```

内容为：

```
model: openrouter/minimax/minimax-m2.7
```

这在以下情况很有用：

* 云端模型用于编程
* 本地 DeepSeek 用于离线工作
* 不同的代码仓库 → 使用不同的模型

---

# 验证当前模型

运行：

```
/model
```

OpenClaw 会打印当前激活的模型。

---

# 典型最佳实践

默认设置：

```
openrouter/minimax/minimax-m2.7
```

需要时切换：

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

这提供了：

* 快速的云端推理
* 经济的本地备用方案
* 离线能力

正符合你代码片段所描述的需求。
