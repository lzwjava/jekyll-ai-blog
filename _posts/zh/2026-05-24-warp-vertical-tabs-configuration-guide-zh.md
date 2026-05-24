---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Warp 垂直标签配置指南
translated: true
type: note
---

**问题：** Warp的垂直标签布局是如何工作的，以及如何配置它？

**答案：**

垂直标签是一个**最近发布的功能**（文档更新于约3天前）。以下是完整介绍：

---

## 启用

导航至 `Settings → Appearance → Tabs`，然后开启 **"Use vertical tab layout"** 开关。

就这样。水平标签栏消失，取而代之的是一个**可调整大小的左侧边栏**。

---

## 侧边栏显示什么

垂直标签面板用侧边栏替换了水平标签栏，显示丰富的元数据、拖放管理以及标签和面板的显示选项。

面板内的关键用户体验功能：

- **紧凑模式与展开模式** — 在紧凑的单行视图（默认）或带有完整元数据的详细多行布局之间选择。
- **可配置的面板标题** — 控制首先显示哪些元数据：最后执行的命令或对话、工作目录或Git分支。
- **悬停详情侧边卡** — 悬停在任何面板行上，可在浮动详情卡片中看到完整、未裁剪的元数据，无需切换焦点。
- **搜索 + 拖放 + 重命名** — 按标题、目录或分支过滤面板；通过拖动重新排序标签或在标签间移动面板；双击标签以直接重命名。

---

## 工具栏控制

可配置工具栏中的"Tabs panel"按钮用于切换垂直标签侧边栏。按钮所在的一侧决定了其面板在窗口的哪一侧打开——因此，如果你希望侧边栏在右侧，可以将该切换按钮移到右侧。

可配置工具栏同时适用于水平标签和垂直标签。

---

## 标签配置（TOML — 可复用的布局）

这是一个与垂直标签配合使用的进阶功能。将标签布局保存为 `.toml` 文件：

```toml
# ~/.local/share/warp-terminal/tab_configs/workstation.toml
[[panes]]
cwd = "~/projects/myrepo"
command = "ssh lzw@192.168.1.36"

[[panes]]
cwd = "~/projects/myrepo"
split_direction = "horizontal"
```

右键点击垂直标签面板或水平标签栏中的任意标签，然后点击 **"Save as new config"** — Warp 会根据标签的布局、命令和目录生成一个 `.toml` 文件。

标签配置文件位于：
```
~/.local/share/warp-terminal/tab_configs/   # stable
~/.local/share/warp-terminal-preview/tab_configs/  # preview
```

新配置会自动出现在 `+` 菜单中。

---

## 适合你工作流的实用布局

假设你拥有 MacBook Air（日常使用）和位于 `192.168.1.36` 的工作站：

```
Vertical sidebar tabs:
├── [local] ~/projects          ← 日常编码
├── [ssh] lzw@192.168.1.36     ← GPU工作站
├── [monitor] nvidia-smi -l 1  ← 训练监视器
└── [logs] tail -f train.log   ← 模型输出
```

将每一个都保存为 Tab Config → 从 `+` 菜单中点击一次即可恢复完整布局。这是相比 iTerm2 的真正优势——无需会话管理器插件，无需本地 tmux，只需要你可以版本控制的 TOML 文件。

---

## 为什么在大规模场景下垂直优于水平

- 水平标签在超过约6个标签时会被截断——你会丢失标签名称
- 垂直侧边栏可扩展到20多个标签，且完整元数据可见
- 每个标签无需切换即可看到 Git 分支和工作目录——在同时处理多个模型训练运行或代理会话时至关重要

参考：

- [Vertical Tabs - Warp 文档](https://docs.warp.dev/terminal/windows/vertical-tabs/)
- [Tab Configs - Warp 文档](https://docs.warp.dev/terminal/windows/tab-configs/)
- [Configurable toolbar - Warp 文档](https://docs.warp.dev/terminal/windows/configurable-toolbar/)