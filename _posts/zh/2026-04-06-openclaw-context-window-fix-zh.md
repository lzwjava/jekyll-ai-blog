---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw上下文窗口修复
translated: true
type: note
---

问题：OpenClaw 为何显示 “Agent failed before reply: Model context window too small (8192 tokens). Minimum is 16000”，应如何解决？

回答：

此错误意味着 **你配置的模型仅支持 8K 上下文窗口**，但 OpenClaw 的智能体 **运行至少需要 16K 词元**。因此智能体在回复前就停止了运行。

### 发生原因

* 你当前的模型：**最多 8,192 个词元**
* OpenClaw 要求：**≥ 16,000 个词元**
* 结果：智能体拒绝启动

这种情况通常在使用以下配置时发生：

* 小型本地 GGUF 模型
* 旧版 Qwen / LLaMA 配置
* 错误的 OpenRouter 模型变体
* llama.cpp 服务器启动时设置了较低的上下文长度

---

# 修复方法（任选其一）

## 方法 1 — 切换到更大上下文的模型（推荐）

使用支持 **16K / 32K / 128K** 上下文的模型。

例如：

* DeepSeek-R1 (32K+)
* Qwen2.5-32B (32K)
* Mistral-Large (32K)
* 通过 OpenRouter 的 Claude / GPT (100K+)

示例（使用 OpenClaw 斜杠命令）：

```
/model openrouter/deepseek/deepseek-r1
```

或

```
/model openrouter/qwen/qwen-2.5-32b-instruct
```

---

## 方法 2 — 增加 llama.cpp 的上下文长度（本地模型）

如果你在运行本地服务器：

以更大的上下文长度启动：

```
--ctx-size 16384
```

或更推荐：

```
--ctx-size 32768
```

示例：

```
llama-server \
  -m DeepSeek-R1.gguf \
  --ctx-size 32768
```

---

## 方法 3 — 降低 OpenClaw 的智能体要求（不推荐）

你可以降低要求，但智能体的质量会下降。

修改 OpenClaw 配置：

```
agent:
  min_context: 8192
```

但这通常会破坏以下功能：

* 规划
* 工具调用
* 长代码编辑

因此，更好的方法是升级模型。

---

## 快速诊断

运行：

```
openclaw model
```

或

```
openclaw doctor
```

你可能会看到：

```
context: 8192
required: 16000
```

---

## 最佳实践选择

使用：

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

因为它支持 **32K 上下文**，并且与 OpenClaw 配合良好。

---

简而言之：

* 此错误属于正常情况
* 你的模型上下文太小
* 切换到 16K+ 上下文的模型
* 或者增加 ctx-size

这些方法将立即解决问题。