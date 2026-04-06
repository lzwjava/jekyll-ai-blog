---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 克劳德工具连接问题
translated: true
type: note
---

**问题**：  
为何 `/home/lzw/projects/llama.cpp/models/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf` 能在 OpenClaw（AI 代理）中运行，但我却收到“Connect your tools to Claude… This isn't working right now”的错误提示？

**回答**：

这**不是模型问题**。你的本地 GGUF 模型能在 OpenClaw 中工作，但该错误源于 **Claude 工具集成**，而非 `llama.cpp` 或模型本身。

你看到的是：

> “Connect your tools to Claude… This isn't working right now. Try again later.”

这通常在 **OpenClaw 切换到 Claude 代理模式**，但**工具服务器 / MCP 桥接未连接**时发生。

因此：

* ✅ 本地模型运行正常 (`DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf`)
* ❌ Claude 工具模式失败（工具连接缺失）
* ❌ 与上下文窗口无关
* ❌ 与 GGUF 无关
* ❌ 与 llama.cpp 无关

---

## 为何 OpenClaw 能与本地模型协同工作

当你运行：

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

时，OpenClaw：

* 使用**本地 llama.cpp 服务器**
* 无需云工具
* 无需 Claude 集成
* 无需 MCP

因此一切正常。

---

## 为何 Claude 模式会失败

当 OpenClaw 切换到 **Claude 工具模式** 时，它期望：

* MCP 工具服务器正在运行
* 工具注册表已连接
* Claude API 会话活跃

若其中一项失败 → 你将看到：

```
Connect your tools to Claude
This isn't working right now
```

这是一个**工具连接错误**，而非推理错误。

---

## 最常见原因

### 1. Claude 工具桥接未启动

你需要类似以下命令：

```
openclaw tools start
```

或

```
openclaw mcp start
```

（具体取决于你的版本）

---

### 2. 意外使用了 Claude 代理

你可能处于：

```
Agent: Claude
```

模式，而非：

```
Agent: Local
```

请切换回本地模式：

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

---

### 3. 工具提供方离线

Claude 工具使用：

* 文件系统
* bash
* git
* 浏览器

若 OpenClaw 无法连接它们 → 报错。

---

## 为何 OpenClaw 仍能运行本地模型

因为 OpenClaw 架构如下：

```
代理层
   ↓
模型层（本地 gguf）
   ↓
工具层（可选）
```

你的模型运行正常，
但 **Claude 代理需要工具**，
因此在推理前就已失败。

---

## 快速修复

使用纯本地代理：

```
/agent local
```

然后：

```
/model llama-server/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

这将完全绕过 Claude 工具。

---

## 另一修复方法

完全重启 OpenClaw：

```
pkill -f openclaw
openclaw dev
```

然后重新加载模型。

---

## 总结

你的模型运行正常 ✅  
Claude 工具未连接 ❌  
OpenClaw 本地模式不受影响 ✅

因此，问题是 **Claude 工具集成**，而非：

* 非 GGUF 问题
* 非 VRAM 问题
* 非上下文问题
* 非 llama.cpp 问题

这是预期行为。

如果你粘贴：

* `openclaw logs --follow`
* 或你的 `/agent` 输出

我可以准确定位是哪一层发生了故障。