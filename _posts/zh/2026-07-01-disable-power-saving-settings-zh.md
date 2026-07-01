---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 禁用省电设置
translated: true
type: note
---

在 `lzwjava@192.168.1.57` (Fedora 44 / GNOME) 上完成：

| 设置 | 之前 | 之后 |
| --- | --- | --- |
| 屏幕保护程序空闲激活 | `true` | **`false`** |
| 锁定屏幕 | `true` | **`false`** |
| 交流电超时后挂起 | 900秒（15分钟） | **0（从不）** |
| 屏幕变暗 | `true` | **`false`** |
| 会话空闲延迟 | 300秒 | **0（从不）** |

与 xiaoxin 的机器行为一致——接通电源时屏幕保持亮着，从不锁定，从不变暗，从不挂起。
