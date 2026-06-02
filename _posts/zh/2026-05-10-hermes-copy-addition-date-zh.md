---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 爱马仕/copy命令添加日期
translated: true
type: note
---

问题：Hermes 中的 `/copy` 命令是何时添加的？

答案：

Hermes 中的 `/copy` 命令由提交 **99fd3b51** 于 **2026-04-09** 添加。该命令本身**不**包含任何计时信息；你在使用 `/copy` 后状态栏中看到的时间元素来自其他提交：

* **Session duration**（`44m`）—— 于 2026 年 3 月 16 日由提交 **00a0c565** 添加。
* **Per-prompt elapsed timer**（`⏲ 10m 19s`）—— 于 2026 年 4 月 20 日由提交 **654d61ab** 添加。

因此，`/copy` 命令独立于这些计时器存在，计时器属于持久化状态栏的一部分。

参考文献：

* [提交 99fd3b51 — 添加 /copy 命令](https://github.com/hermes-agent/hermes/commit/99fd3b51)
* [提交 00a0c565 — 持久化 CLI 状态栏](https://github.com/hermes-agent/hermes/commit/00a0c565)
* [提交 654d61ab — 每次提示的耗时计时器](https://github.com/hermes-agent/hermes/commit/654d61ab)
