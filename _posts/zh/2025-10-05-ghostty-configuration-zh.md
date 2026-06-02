---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 理解Ghostty配置文件
translated: true
type: note
---

### Ghostty 配置文件工作机制

Ghostty 的配置文件采用简单的基于文本的键值对格式，样式为 `key = value`。它的设计直观明了，让你只需覆盖关心的默认设置——Ghostty 为其他所有选项都内置了合理的默认值，因此最小化甚至空的配置文件也能正常工作。

#### 语法速览
- **键与值**：键名始终为小写且区分大小写（例如 `font-family = JetBrains Mono`）。若值不含空格或特殊字符则无需引号（例如 `font-family = "JetBrains Mono Nerd Font"`）。等号 `=` 周围的空格不影响解析。
- **注释**：在行首使用 `#` 添加注释（例如 `# 我的自定义主题`）。不支持在值后添加行内注释，否则会被解析为值的一部分。
- **重置为默认值**：使用空值如 `key =` 可将设置恢复为 Ghostty 的内置默认值。
- **特殊值**：部分选项具有独特格式，例如时长（如 `resize-overlay-duration = 4s 200ms`）——具体请查阅文档。
- **文件加载**：Ghostty 在 `~/.config/ghostty/config`（Linux/Windows）或 `~/Library/Application Support/com.mitchellh.ghostty/config`（macOS）路径查找配置文件。可通过 `config-file = path/to/other.conf` 引入其他文件实现模块化配置。
- **命令行覆盖**：所有设置均可通过命令行参数指定（例如 `ghostty --font-family="Fira Code"`），其优先级高于配置文件。

修改配置后，通过默认快捷键（macOS 为 Cmd+Shift+,，Linux/Windows 为 Ctrl+Shift+,）或运行 `ghostty +reload-config` 可立即生效。

要查看所有选项及默认值，请在终端中运行 `ghostty +show-config --default --docs`。

### 典型配置示例
“典型”配置通常极为精简——仅调整字体、色彩或边距等基础设置以提升使用体验。Ghostty 的默认设置包含 JetBrains Mono 字体家族（内置 Nerd Font 支持）、纯净的背景/前景配色方案，且无额外边距。

以下是一个简单的深色主题配置示例，采用流行字体、适当边距及基础键位绑定。将此保存为你的 `config` 文件即可：

```
# 带边距与自定义字体的基础深色主题
background = 1e1e1e
foreground = f8f8f2
font-family = "JetBrains Mono Nerd Font"
font-size = 14

# 为文本周围添加呼吸空间
window-padding-x = 8
window-padding-y = 8

# 自定义键位绑定（如需覆盖默认设置）
keybind = cmd+t=new_tab
keybind = cmd+w=close_tab
keybind = cmd+d=new_split:right
```

这份配置在保持轻量化的同时完成了核心定制。你还可以通过文档中的调色板配置（如 `color0 = 282a36`）或主题设置进行扩展。

[Ghostty 配置文档](https://ghostty.org/docs/config)
