---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 私人笔记标记已添加
translated: true
type: note
---

已完成。以下是 `~/.pi/agent/extensions/note/index.ts` 中的更改：

| 更改 | 详情 |
|--------|--------|
| **`WwQueueEntry` 接口** | 添加了 `private?: boolean` 字段 |
| **`enqueue()` 函数** | 添加了 `isPrivate` 参数，传入时设置 `entry.private = true` |
| **`handleNote()` 函数** | 解析 `--private` 标记，将 `isPrivate` 传递给 `enqueue()` |
| **输出消息** | 使用该标记时显示 `(private)` 标签 |
| **文档注释** | 添加了 `--private` 使用示例 |

现在，pi agent 的 `/note --private` 会在队列中入队一个带有 `"private": true` 的笔记，而 `ww note process` 处理器会将其保存到 `/Users/lzwjava/projects/jekyll-ai-blog/private-note` 且不执行 git push。