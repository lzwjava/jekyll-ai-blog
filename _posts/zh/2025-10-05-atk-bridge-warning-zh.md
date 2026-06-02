---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 理解atk-bridge警告信息
translated: true
type: note
---

这条警告信息出现在 Linux 系统（特别是 Ubuntu）上基于 GTK 的应用程序中（如 Firefox、Snap Store 或 GitHub CLI）。它并非错误——只是提示信息。"atk-bridge" 模块曾用于连接无障碍工具包（ATK）以支持屏幕阅读器等无障碍功能，但新版 GTK（约从 3.22 开始）已直接内置该功能。加载独立模块显得多余，因此 GTK 会跳过并记录此提示。

该提示不影响应用程序性能，但若终端输出显示杂乱，可通过设置环境变量 `NO_AT_BRIDGE=1` 来屏蔽。例如：

```bash
export NO_AT_BRIDGE=1
firefox  # 或触发该提示的其他应用
```

如需永久设置，请将 export 命令行添加到 `~/.bashrc` 或 `~/.profile` 文件中。

### 参考资料

- [不加载模块"atk-bridge"：该功能已由 GTK 原生提供](https://stackoverflow.com/questions/75406844/not-loading-module-atk-bridge-the-functionality-is-provided-by-gtk-natively)
- [启动 firefox 时出现错误：不加载模块"atk-bridge"](https://askubuntu.com/questions/1462267/when-launching-firefox-get-error-not-loading-module-atk-bridge)
- [运行任何 gh 命令时提示：不加载模块"atk-bridge"](https://github.com/cli/cli/issues/9043)
