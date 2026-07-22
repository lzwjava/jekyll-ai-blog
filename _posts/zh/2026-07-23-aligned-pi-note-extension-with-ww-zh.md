---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 对齐Pi音符扩展与ww
translated: true
type: note
---

所有内容已整理完毕。以下是已完成的工作：

## 修复摘要

**问题**：Pi 代理的 `/note` 扩展将内容写入 `~/.config/pi/note_queue.json` 而非 `~/.config/ww/note_queue.json`，并且使用的 JSON 格式与 ww 笔记监控程序（`ww note watch`）所期望的格式不同。

### 对 `/home/lzw/.pi/agent/extensions/note/index.ts` 的修改

1. **路径**：`~/.config/pi/note_queue.json` → `~/.config/ww/note_queue.json`
2. **队列格式**：从 `{entries: [...]}` 包装结构改为**纯 JSON 数组**（与 `ww/note/note_queue.py` 一致）
3. **条目字段**：现在以 ww 兼容格式写入条目：
   - `content`（原为 `text`）
   - `content_hash` — SHA-256 前 12 位字符（原为随机 shortId）
   - `queued_at` — 精确到秒的 ISO 时间戳（原为 `timestamp`）
   - `status: "pending"` — 确保监控程序能识别
   - `type: "note"`、`note_path: null`
   - `id` — 现在使用内容哈希（与 ww 相同）替代随机值
4. **去重**：新增重复内容检查（相同哈希且状态为 pending），与 ww 行为一致
5. **错误处理**：向用户显示错误信息（如重复内容）

### 数据迁移

已将 **9 条独立条目** 从旧的 pi 队列迁移至正确的 ww 队列（其中 2 条重复内容已去重）。所有条目均为 `status: "pending"` 状态，可供 `ww note watch` 守护进程处理。
