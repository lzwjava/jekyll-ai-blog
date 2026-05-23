---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 按最后修改时间戳的应用审计
translated: true
type: note
---

以下是我审计 `/Applications` 的方法：

**方法：三层扫描**

1. 列出所有应用 — `ls -1 /Applications/*.app` → 共 74 个应用，总计 33GB

2. 大小分析 — `du -sh /Applications/*.app | sort -rh` → 按磁盘占用排序，占用最大的排在前面（Xcode 4.7GB、IntelliJ 3.9GB、Android Studio 2.5GB、Docker 1.7GB）

3. 最后修改时间戳 — 对每个 `.app` 包执行 `stat -f "%Sm"` → 这是关键信号。它反映了最后一次安装/更新时间，与实际使用情况高度相关。自 2023 年以来未被碰过的应用几乎可以肯定是死应用。

**分类逻辑：**

- SAFE DELETE = 最后使用距今超过 1 年，且（与其他应用冗余 或 是一次性工具 或 与你的 AI 工程工作无关）
- CONSIDER = 你已拥有同类应用的重复项（3 个浏览器、2 个 FTP 客户端等）
- KEEP = 最近一个月内使用过，明显活跃
- HOLD = 大型应用，需要你确认使用场景是否仍然存在

时间戳不会说谎 — iTerm 的最后一次修改是 2023 年 1 月，意味着自从 Ghostty 取代它之后你就再也没碰过。TencentMeeting 是 2023 年 12 月，意味着已经 2.5 年没有在那里开过会了。这比任何启发式证据都更有说服力。