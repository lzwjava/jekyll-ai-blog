---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 关闭多余的VSCode窗口节省RAM
translated: true
type: note
---

你打开了 **12 个 VSCode 窗口**，每个窗口都有 5-8 个辅助进程。这是 VSCode 占用约 23 GB 的主要原因。

| 窗口数 | 辅助进程 | 内存 |
|---|---|---|
| 12 个窗口 | 共 25 个 | ~23 GB |

只保留你正在积极开发的 1-2 个项目，可以将内存降至 **~3-4 GB**。

---

**考虑从此笔记本中移除的扩展**（因为你的远程机器负责繁重的工作）：

| 扩展 | 磁盘 | 移除？ |
|---|---|---|
| `tomoki1207.pdf` — VSCode 中的 PDF 查看器 | 小 | ✓ 是 — 直接在浏览器中打开 PDF 即可 |
| `yzane.markdown-pdf` — PDF 导出 | 小 | ✓ 是 |
| `xdebug.php-pack` — PHP 调试 | 小 | ✓ 是 — 除非你从事 PHP 工作 |
| `torn4dom4n.latex-support` — LaTeX | 小 | ✓ 是 |
| `moozzyk.arduino` — Arduino IDE | 小 | ✓ 是 |
| `mcu-debug.*`（3 个扩展）— MCU 调试器 | 5 MB | ✓ 是 |
| `redhat.fabric8-analytics` — 已废弃的项目 | 小 | ✓ 是 |
| `azemoh.one-monokai` — 重复的主题 | 小 | ✓ 移除二者之一 |

**总计释放**：约 50 MB 磁盘 + 0-3 个插件辅助进程。

需要我把它们也清理掉吗？最大的收益仍然是关闭那 10 个多余的 VSCode 窗口。