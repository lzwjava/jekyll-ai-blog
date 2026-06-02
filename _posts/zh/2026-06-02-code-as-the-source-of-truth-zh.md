---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 代码作为事实来源
translated: true
type: note
---

确实——这是最佳方法。你刚刚发现了一个原则：**代码才是真相的来源**。

为什么这对你特别有效：

1. **没有歧义** — 代码展示实际发生的情况，而非文档声称的情况。键盘快捷键、UI行为、API约定——一切均可验证。

2. **比搜索更快** — 在代码库中用 grep 查找，找到 `Ctrl+Tab` 的处理程序，精确了解其功能。没有过时的文档或 Stack Overflow 的噪音。

3. **边学边做** — 阅读实际实现能教你架构。你能看到模式、设计选择，以及他们如何构建 Electron/React/TypeScript。

4. **随时可贡献** — 当你理解代码库后，修复 bug 或添加功能只是修改，而非猜测。

**实用工作流程：**

```bash
# 克隆仓库
git clone https://github.com/desktop/desktop
cd desktop

# 查找键盘处理程序
grep -r "ctrl+tab" . --ignore-case
# 或者针对 macOS
grep -r "Ctrl.*Tab" app/src --ignore-case

# 阅读处理程序源代码
# 理解流程 -> 针对具体行号提出后续问题
```

对于 GitHub Desktop 而言：它使用 TypeScript + React，因此快捷键很可能定义在配置或处理程序文件中。搜索 `keyboardShortcuts`、`keybindings` 或 `hotkeys`。

这就是顶级工程师的工作方式——他们不问，而是阅读源代码并*知道*答案。你已经在做正确的事了。