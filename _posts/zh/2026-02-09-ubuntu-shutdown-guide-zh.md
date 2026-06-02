---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Ubuntu 关机命令指南
translated: true
type: note
---

**Question:** 如何在 Ubuntu 中运行 "shutdown now"？

**Answer:**

以下是在终端中立即关闭 Ubuntu 的正确且常用的方法：

### 最推荐的现代方法 (Ubuntu 18.04 → 2026)

```bash
# 最整洁且当今最常用的方式
sudo systemctl poweroff

# 立即关机（在大多数情况下与上述相同）
sudo poweroff

# 同样有效的替代拼写
sudo shutdown now
```

### 所有实际有效的变体

| Command                        | What it does                              | Needs sudo? | Notes                                      |
|-------------------------------|--------------------------------------------|-------------|--------------------------------------------|
| `sudo systemctl poweroff`     | 最现代且推荐的方式                          | Yes         | 2020–2026 年最整洁的方法                   |
| `sudo poweroff`               | 简单的快捷方式                              | Yes         | 非常常用                                   |
| `sudo shutdown now`           | 经典的 System V 风格命令                    | Yes         | 仍然有效，但被视为旧版方式                 |
| `sudo shutdown -h now`        | 与上述相同（更明确）                        | Yes         | -h = halt/poweroff                         |
| `sudo init 0`                 | 非常老派的方式                              | Yes         | 有效但现在几乎不再使用                     |
| `sudo reboot`                 | 重启而非关机                                | Yes         | 仅供参考                                   |
| `sudo systemctl reboot`       | 现代的重启方式                              | Yes         | —                                          |

### 快速“我只想立即关机”备忘单

任选其一 —— 它们在 2025/2026 年都有效：

```bash
sudo poweroff
# 或者
sudo systemctl poweroff
# 或者（仍然有效）
sudo shutdown now
```

### Bonus: 人们通常使用的最客气的方式

```bash
# 现实世界中人们实际使用的最常见命令：
sudo shutdown -h now
```

所有这些命令都会整洁地关闭应用程序并立即关闭计算机电源。

**References:**
- 无需（这是近期各版本 Ubuntu 的标准行为）
