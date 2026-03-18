---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Code CLAUDE.md 文件合并在一起
translated: true
type: note
---

问题：当项目级 `CLAUDE.md` 和全局 `~/.claude/CLAUDE.md` 同时存在时，两者都会生效还是只有项目级的生效？回答：

**两者同时生效** — 它们被合并，而不是互斥。

### 工作原理

当您在项目文件夹中启动会话时，Claude Code 会读取两个文件。全局文件先加载，然后项目级文件叠加在其上。因此，如果您的全局文件说 "always explain things step by step"，而您的项目文件说 "this site uses WordPress with a custom theme"，Claude 会同时执行两者。

### 加载顺序与优先级

当您启动 Claude Code 时，它会从运行 `claude` 的目录向上遍历目录树，加载沿途发现的每个 `CLAUDE.md` 文件。每个祖先目录都会被检查。指令会合并在一起，较近的文件优先于较远的文件。

优先级栈（最高 → 最低）：

```
Project CLAUDE.md          ← 最高优先级
Parent directory CLAUDE.md
...ancestor directories...
~/.claude/CLAUDE.md        ← 最低优先级（全局）
```

### 冲突解决

如果同一指令出现在多个级别，更具体的层级获胜。例如：全局说 "Use 2-space indentation"，项目说 "Use 4-space indentation" — 项目针对该项目获胜。

### 实用心智模型

您的全局文件是放置让 Claude 感觉已经了解您的事项的地方 — 您的偏好、您的风格、您的工作习惯。您的项目级文件是放置让 Claude 在特定代码库中有效的事项的地方。如果信息是关于**您**的，则放入全局。如果信息是关于**项目**的，则放入项目文件夹。

### 总结

| 文件                  | 作用域       | 用途                          |
|-----------------------|--------------|-------------------------------|
| `~/.claude/CLAUDE.md` | 所有项目     | 个人风格、编码原则、全局规则  |
| `./CLAUDE.md` (项目)  | 仅此项目     | 技术栈、架构、项目特定规则    |

因此，您的全局编码原则（如 Wang Yin 的规则）非常适合 `~/.claude/CLAUDE.md`，而项目特定上下文（例如 "this uses Next.js + Prisma"）属于项目级文件。

参考资料：

- [Claude Code Memory Files: Global vs Project Level](https://raythanni.substack.com/p/claude-code-memory-files-global-vs)
- [CLAUDE.md Files and Memory Hierarchy](https://deepwiki.com/FlorianBruniaux/claude-code-ultimate-guide/4.1-claude.md-files-and-memory-hierarchy)
- [Mastering CLAUDE.md: Multi-Project Workflows](https://www.shahabpapoon.com/blog/mastering-claude-md-multi-project-workflow/)