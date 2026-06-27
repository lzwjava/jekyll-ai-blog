---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes插件未启用修复
translated: true
type: note
---

**问题：** 在 Hermes CLI 中，`/note` 命令返回 "Unknown command: /note"。

**调查过程：**

1. 插件源码存在于两个位置：
   - `~/projects/config/hermes/plugins/note/`（配置仓库）
   - `~/.hermes/plugins/note/`（Hermes 插件目录）
   - 两者内容相同（diff 显示无差异）

2. 插件文件有效：
   - `plugin.yaml` — 正确的清单（名称、版本、描述）
   - `__init__.py` — 包含正确的 `register(ctx)` 函数，该函数调用 `ctx.register_command("note", ...)`
   - 处理器通过 `ww.note.create_note_from_clipboard` 将最后一条助手响应保存为 markdown 笔记
   - 支持参数：`[number] [--title <title>] [--dir <dir>]`
   - 保存后自动执行 git commit 并推送

3. 插件发现正常——文件位于 Hermes 查找的 `~/.hermes/plugins/note/` 目录下

4. **根本原因：** `~/.hermes/config.yaml` 中 `plugins.enabled: []` ——空列表意味着即使正确安装了插件，也不会加载任何插件

**修复：** 将 `~/.hermes/config.yaml` 中的 `plugins.enabled: []` 改为 `plugins.enabled: [note]`。需要重启 Hermes 才能生效。

**关键要点：** Hermes 插件系统需要满足两个条件：（1）插件文件位于 `~/.hermes/plugins/<name>/` 目录下；（2）插件名称必须在 config.yaml 的 `plugins.enabled` 列表中列出。缺少步骤 2 会导致插件被静默忽略。