---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ghostty 终端字体大小增大
translated: true
type: note
---

**问题：** 由于我主要在终端中工作（例如使用 Hermes agent 等），同时我有近视，我能否直接放大 Ghostty 终端的字体大小来更清晰地查看？

**回答：**

当然可以！增大 Ghostty 的字体大小是帮助眼睛的最简单有效的方法之一——尤其是正如你在视力技巧博客中所描述的，你已经通过欠矫眼镜管理近视，并且大部分时间在终端中工作。更大的文字意味着更少的眼疲劳，无需更换处方。

---

## 如何在 Ghostty 中增大字体大小

### 方法 1：键盘快捷键（即时生效，运行时）

在 **macOS** 上：
- **增大字体大小：** `Cmd` + `+`
- **减小字体大小：** `Cmd` + `-`
- **重置字体大小：** `Cmd` + `0`

在 macOS 上，Ghostty 默认的增大/减小字体快捷键分别是 `Cmd + +` 和 `Cmd + -`。

在 **Linux** 上，你可以使用诸如 `super+equal` 或 `super+plus` 来增大字体大小，`super+minus` 来减小字体大小。

---

### 方法 2：配置文件（永久生效）

编辑 Ghostty 配置文件（在应用中用 `Command + ,` 打开），设置 `font-size` 为你想要的值，例如 `font-size=14`。

为了更好的可读性，你可能想设得更高——例如 `font-size=18` 或 `font-size=20`：

```ini
font-size = 18
font-thicken = true
```

`font-thicken 可以使终端字体变粗，提高可读性。

编辑后，右键点击终端窗口，选择 Config → Reload Configuration 即可应用更改，无需重启。

---

### 方法 3：自定义快捷键（适用于所有标签页/分屏）

你可以在配置中添加明确的快捷键，使字体大小更改应用于所有标签页：

```ini
keybind = all:super+zero=reset_font_size
keybind = all:super+equal=increase_font_size:1
keybind = all:super+plus=increase_font_size:1
keybind = all:super+minus=decrease_font_size:1
```

---

### 方法 4：通过命令行

你也可以通过命令行选项传递字体大小：`--font-size=12` 或 `--font-family="Fira Code"`。

---

## 为什么这对你的情况很有效

由于你大部分时间都在终端中工作（Hermes agent、Claude Code 等），增大 Ghostty 的字体大小非常理想：

- **无需更换眼镜**——只需要更大的屏幕文字**
- 它与你博客中提到的“刚好清晰”的欠矫原则相辅相成——你使用低度数眼镜，而更大的文字弥补了轻微模糊
- 非常适合终端密集型工作流（编程、agent、CLI 工具）
- 你甚至可以通过 action 设置特定的字体大小：`set_font_size:14.5` 会将字体大小设置为 14.5 磅。

一个不错的起点是 `font-size = 18` 或 `font-size = 20`，然后根据喜好调整。

---

**参考链接：**

- [Ghostty 配置参考 - ghostty.org](https://ghostty.org/docs/config/reference)
- [Ghostty 快捷键操作参考 - ghostty.org](https://ghostty.org/docs/config/keybind/reference)
- [我的小 Ghostty 终端配置 - birchtree.me](https://birchtree.me/blog/my-lil-ghosty-terminal-config-2/)
- [在所有标签页中增大字体大小 - GitHub 讨论](https://github.com/ghostty-org/ghostty/discussions/8149)
