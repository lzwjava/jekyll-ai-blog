---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pi Agent 笔记扩展
translated: true
type: note
---

以下是你创建的 Pi Agent **笔记扩展** (`~/.pi/agent/extensions/note/index.ts`) 的摘要：

---

## 功能说明

注册 `/note` 命令，捕获助手回复并将其以 JSON 数组形式追加到 `~/.config/pi/note_queue.json` 文件中——与你的 Hermes 插件使用相同的队列模式。

## 实现方式

| 特性 | 实现细节 |
| --- | --- |
| **`/note`** | 将最后一条非空助手回复加入队列 |
| **`/note 3`** | 将第 3 条助手回复加入队列 |
| **`/note --title "我的标题"`** | 为队列条目添加 `title` 字段 |
| **推理标签** | 自动移除 `<thinking>`、`<reasoning>`、`<scratchpad>` 标签 |
| **队列文件** | `~/.config/pi/note_queue.json`——包含 `{id, timestamp, title?, text}` 对象的数组 |

## Pi 与 Hermes API 映射

| Hermes (Python) | Pi Agent (TypeScript) |
| --- | --- |
| `ctx.register_command("note", ...)` | `pi.registerCommand("note", { ... })` |
| `cli.conversation_history` | `ctx.sessionManager.getEntries()`（按 `type: "message"` + `role: "assistant"` 过滤） |
| `ctx._manager._cli_ref` | 无需访问私有字段——使用稳定的公共 API |
| 插件位于 `~/.hermes/plugins/note/` | 扩展位于 `~/.pi/agent/extensions/note/index.ts` |

## 使用方法

由于扩展位于 `~/.pi/agent/extensions/note/index.ts`，Pi Agent 会在启动时自动发现。在活动会话中运行 `/reload` 即可加载，然后：

```
/note                              # 将最后一条回复加入队列
/note 2 --title "重构计划"          # 将第 2 条回复加上标题后加入队列
```

外部守护进程（如你的 `ww note watch`）可以轮询 `~/.config/pi/note_queue.json` 并处理新条目。
