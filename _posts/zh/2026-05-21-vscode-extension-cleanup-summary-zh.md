---
audio: false
generated: true
image: false
lang: zh
layout: post
title: VSCode扩展清理摘要
translated: true
type: note
---

所有10个已移除。清理摘要：

| 已移除 | 状态 |
|---|---|
| `tomoki1207.pdf` — PDF 查看器 | 已移除 |
| `yzane.markdown-pdf` — PDF 导出 | 已移除 |
| `xdebug.php-pack` — PHP | 已移除 |
| `torn4dom4n.latex-support` — LaTeX | 已移除 |
| `moozzyk.arduino` — Arduino | 已移除 |
| `mcu-debug.*`（3个 MCU 调试器） | 已移除 |
| `redhat.fabric8-analytics` | 已移除 |
| `azemoh.one-monokai` — 重复主题 | 已移除 |
| `vadimcn.vscode-lldb`（7个旧版本） | 之前已移除 |
| **总计：59 → 42 个扩展目录** | **已移除 17 个** |

**最大的剩余优化**是关闭多余的 VSCode 窗口。你当前**打开了 12 个**窗口。每个窗口会衍生约 5 个辅助进程。如果关闭其中 10 个，VSCode 的内存占用将从约 23 GB 瞬间降至约 3-4 GB。

`Cmd+Q` 关闭那些你不在这台笔记本上编辑的窗口（将繁重的编码工作留给远程机器）。
