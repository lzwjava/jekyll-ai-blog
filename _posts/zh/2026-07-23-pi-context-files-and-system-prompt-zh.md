---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pi上下文文件和系统提示
translated: true
type: note
---

是的。每次会话时，Pi 都会加载 `**AGENTS.md**`（或 `CLAUDE.md`）作为上下文文件。根据 README 的**Context Files**部分：

> Pi 在启动时从以下位置加载 `AGENTS.md`（或 `CLAUDE.md`）：
>
> - `~/.pi/agent/AGENTS.md`（全局）
> - 父目录（从当前工作目录向上查找）
> - 当前目录

所有匹配的文件会通过从当前工作目录向上查找的方式找到，然后拼接并注入到系统提示中。对于 `/home/lzw/projects/pi` 这个项目，仓库根目录中的 `AGENTS.md` 文件就是我加载并遵循的项目规则。

你还可以在交互式启动的头部信息中看到哪些 `AGENTS.md` 文件被加载了。使用 `--no-context-files` / `-nc` 可以禁用加载。

此外还有 `**SYSTEM.md**`（`.pi/SYSTEM.md` 或 `~/.pi/agent/SYSTEM.md`）用于完全替换系统提示，以及 `**APPEND_SYSTEM.md**` 用于追加而不替换。
