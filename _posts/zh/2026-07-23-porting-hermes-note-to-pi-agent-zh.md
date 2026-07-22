---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将Hermes笔记移植到Pi代理
translated: true
type: note
---

以下是我们的工作摘要：

## 摘要

**1. 探索项目** — 你向我展示了当前工作目录（`/mnt/data/zz`），这是一个用于下载、提取、分词和分析大型数据集（FineWeb、Wikimedia 等）以进行模型训练的**机器学习数据管道**。

**2. 研究 Pi Agent 扩展 API** — 你分享了自己的 Hermes `note` 插件（一个通过 `/note` 将助手响应加入队列的 Python 插件），我阅读了完整的 Pi Agent 扩展文档，包括 `extensions.md`、`session-format.md` 以及多个示例（`bookmark.ts`、`summarize.ts`）。

**3. 构建了一个 Pi Agent 笔记扩展** — 我在 `~/.pi/agent/extensions/note/index.ts` 编写了一个等效的 **TypeScript 扩展**，该扩展：

- 注册了一个 `/note` 命令
- 通过 `ctx.sessionManager.getEntries()` 获取会话中最后一条（或第 N 条）助手响应
- 移除思考/推理标签
- 将结果以 JSON 条目形式追加到 `~/.config/pi/note_queue.json`
- 支持 `--title "..."` 和可选的响应编号参数

**关键映射：**

- Hermes（Python） → Pi Agent（TypeScript）
- `ctx.register_command()` → `pi.registerCommand()`
- 私有 `ctx._manager._cli_ref` → 稳定公开 `ctx.sessionManager.getEntries()`
- 插件目录 `~/.hermes/plugins/note/` → 扩展目录 `~/.pi/agent/extensions/note/index.ts`
