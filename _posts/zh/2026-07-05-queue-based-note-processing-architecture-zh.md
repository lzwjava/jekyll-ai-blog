---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于队列的笔记处理架构
translated: true
type: note
---

完成。以下是修正后的架构：

---

## 笔记插件 — 基于队列的架构

**变更内容**：`/note` 斜杠命令不再直接处理响应，而是将文本内容**加入队列**，由独立的 `ww note watch` 守护进程拾取处理。

**流程**：

```
/note （Hermes CLI）
  └→ 将文本加入队列 → ~/.config/ww/note_queue.json
                        │
            ┌───────────┴───────────┐
            │                       │
   ww note watch              cron: 每30分钟
   （守护进程，轮询间隔3秒）     （安全网）
            │                       │
            └───────────┬───────────┘
                        ↓
               ww note process
                  ├─ LLM 标题生成
                  ├─ 写入 markdown 文件
                  ├─ 修复 MathJax 和表格
                  ├─ git 提交并推送
                  └─ 从队列中清除已完成项
```

**运行中的进程**：

- `ww note watch` — 守护进程 PID **133147**（7月3日启动，仍活跃）
- Hermes 定时任务 `ww-note-process` — 每30分钟运行一次，作为守护进程崩溃时的安全网

**插件**（`~/.hermes/plugins/note/__init__.py`）：

- `/note` → `_enqueue(text, "note")` → 写入 `~/.config/ww/note_queue.json`
- `/note 3` → 将第3条响应加入队列
- `/note --title "Foo"` → 在队列条目中存储标题提示
- 插件本身不调用LLM、不写入文件、不执行git操作 — 仅快速入队

**依赖项**：Hermes 虚拟环境中安装了 `ww` 包，同时也安装了 `pyperclip`。
