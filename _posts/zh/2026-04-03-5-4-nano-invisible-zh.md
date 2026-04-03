---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VSCode中5.4版本Nano无法显示
translated: true
type: note
---

**问题：** 为什么我在 VSCode 中看不到 **5.4 nano**，尽管在 GitHub Copilot 企业版网页上已启用？

**回答：**

这是正常情况。在 GitHub Copilot Enterprise 中，**“管理员端启用” ≠ “在 VSCode 模型选择器中可见”**。
这里有 **三道独立的关卡**：

1. 组织启用的模型
2. 功能向 IDE 的推送部署
3. Agent 模式支持的模型

任何一道关卡缺失 → 你就看不到 **5.4 nano**。

---

# 最常见的原因

### 1. VSCode 扩展版本过旧（最常见）

5.4 / nano 模型只在 **新版 Copilot Chat 构建** 中出现。

请更新以下两者：

* GitHub Copilot
* GitHub Copilot Chat

在 VSCode 中：

```
扩展 → GitHub Copilot → 更新
扩展 → GitHub Copilot Chat → 更新
```

然后重新加载：

```
开发者：重新加载窗口
```

这通常就能解决问题。

---

# 2. 模型为组织启用，但未对聊天启用

企业管理面板有 **独立的开关**：

* 行内补全模型
* 聊天模型
* Agent 模型

有时管理员仅启用：

```
5.4 nano → 仅限行内补全
```

因此你不会在 **Agent 模型选择器** 中看到它。

---

# 3. Agent 模式只显示“支持 Agent”的模型

有些模型是：

* 仅限聊天
* 仅限行内补全
* 支持 Agent

如果 5.4 nano 是 **为行内补全优化的**，它可能不会出现在 Agent 中。

这种情况下，Copilot 内部会使用：

```
Agent 规划器 → 5.4
执行器 → 5.4 nano
```

但 UI 只显示 **5.4**

所以你 *正在使用 nano*，只是无法选择。

---

# 4. 企业策略隐藏了模型选择器

有些组织会锁定：

* 默认模型
* 隐藏下拉菜单
* 强制使用允许的列表

那么 VSCode 只会显示：

```
默认（由组织管理）
```

但后端仍在使用 nano。

---

# 如何验证实际使用情况

打开 VSCode：

命令面板：

```
Copilot: 显示调试信息
```

或

```
Copilot: 打开日志
```

你可能会看到：

```
model: gpt-5.4
executor: gpt-5.4-nano
mode: agent
```

这确认了 nano 正在被使用。

---

# 另一种方法：检查状态栏

VSCode 右下角：

有时会显示：

```
Copilot: GPT-5.4 (Agent)
```

即使执行器是 nano。

这是预期情况。

---

# 关键点

Copilot 架构：

```
Agent 规划器 → 更大的模型
执行 → nano
编辑 → nano
```

UI 只显示规划器模型。

所以你不会总是看到 nano。

---

# 如果你真的希望它可以被选择

你需要：

* 最新的 Copilot Chat
* 模型选择器已启用
* 组织允许手动选择
* nano 被标记为 Agent 模型

否则，它仅在后端使用。

---

**简短回答：**

你很可能 **已经在使用 5.4 nano**，但它是内部使用的，不会显示在 VSCode UI 中。