---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Claude 简历命令简易指南
translated: true
type: note
---

**Question:** 解释 Claude 的 resume command

**Answer:**

`--resume` command（有时也简称为 `/resume`）是 **Claude.ai** 聊天界面（Web 端、桌面应用和移动端 App）内置的一个特殊功能，让你通过引用唯一的 conversation ID 瞬间跳回到之前的任何对话中。

### 工作原理

典型语法：

```
claude --resume 4cb1fd80-1234-5678-9abc-def012345678
```

或者 Claude 通常也接受的简短版本：

```
--resume 4cb1fd80
/resume 4cb1fd80
claude resume 4cb1fd80
```

- 该编号（例如 `4cb1fd80`）是 **缩短后的 conversation UUID**
  当你询问 Claude “what is my current conversation id” 时，或者在分享链接 / 调试信息中，Claude 通常在 UI 中仅显示前 8 个字符。

### 主要使用场景

1. **重新唤起从历史记录中消失的老对话**
   → 极长的对话有时会从侧边栏消失。使用 `--resume <id>` 可以立即将其找回。

2. **在不同设备 / 浏览器间继续同一线程**
   → 在一台设备上复制 ID，在另一台设备上输入 `--resume <id>` → 即可加载相同的聊天内容。

3. **误开启新对话后进行恢复**
   → 无需复制粘贴之前的 50 条消息，直接 resume 旧对话即可。

4. **分享 / 书签特定对话**
   → 用户有时会在 Discord / 论坛中分享 short ID，以便他人加载完全相同的对话状态（前提是该对话在其账号下仍可访问）。

### 如何查找 conversation ID

- 在任何聊天中直接询问 Claude：
  “What is the short ID of this conversation?”
  → 它通常会回复类似于 `Current short ID: 4cb1fd80` 的内容。

- 在分享链接中：
  `https://claude.ai/share/4cb1fd80-…` → 前 8 位字符即为 short ID。

- 切换聊天时，有时可以在浏览器开发者工具（dev tools）或 URL 参数中看到。

### 限制条件

- 仅在 **Claude.ai / Claude apps** 内部有效（在 Grok、Poe 或第三方客户端中无效）。
- 要求你必须登录创建或打开该对话的同一个 **Anthropic account**。
- 非常久远的对话（数月或数年前）即使有 ID，最终也可能变得无法访问。
- 通常 8 位短版本即可生效，但有时需要完整的 UUID。

简而言之：`--resume <id>` 是 Claude 内置的“通过 ID 加载对话”的传送指令 —— 这是一个非常实用的 power-user 功能，特别是对于那些会生成数十个长线程的用户。

**References:**

- None