---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WeType 已彻底移除并清理
translated: true
type: note
---

WeType 已彻底清除：

| 位置 | 状态 |
|---|---|
| `/Library/Input Methods/WeType.app` | 已移除 |
| Launch agent (running process) | 已终止 + 取消注册 |
| `~/Library/Preferences/` | 已清理 |
| `~/Library/Caches/` | 已清理 |
| `~/Library/Application Support/` | 已清理 |
| `~/Library/HTTPStorages/` | 已清理 |
| `~/Library/WebKit/` | 已清理 |
| 诊断日志 | 已清理 |

**节省了约 1.6 GB。** 你需要手动添加 Apple 拼音：

```
系统设置 > 键盘 > 输入法 > 添加 > 中文 > 拼音 - 简体
```