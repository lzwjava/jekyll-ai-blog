---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 标签杀手命名规范合理性
translated: true
type: note
---

**问题：** 存储库/工具应命名为 `tabs-killer` 还是 `tab-killer`？

**回答：**

`tab-killer` — 单数形式。

**理由：**

该工具杀死的是 *标签页的概念*（或泛指的标签页），而非一个名为“tabs”的特定集合。CLI 工具惯例使用单数名词来表示其操作对象：

- `file-watcher`，而非 `files-watcher`
- `process-killer`，而非 `processes-killer`
- `port-scanner`，而非 `ports-scanner`
- `vim` 杀死缓冲区，`grep` 查找行 — 始终使用单数

命名模式为 `<单数名词>-<动词执行者>`。你在构建一个 *tab killer*（标签页杀手），就像 *bug killer*（杀虫剂）一样 — 而不是 *bugs killer*（虫子杀手）。

**`tabs-killer` 读起来语法别扭** — 听起来像非母语者表述的“a killer of tabs”。`tab-killer` 是地道的英语，并且符合 CLI 工具命名惯例。

**建议：** 重命名为 `tab-killer`。由于这是你自己的仓库，只需在 GitHub 上重命名并更新 README。如果你有任何指向它的别名或脚本，一次 sed 替换即可修复：

```bash
sed -i 's/tabs-killer/tab-killer/g' ~/.zshrc ~/.bashrc ~/your-scripts/**/*.sh
```