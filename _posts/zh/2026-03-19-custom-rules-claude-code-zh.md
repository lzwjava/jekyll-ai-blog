---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude 代码中的自定义规则 CLAUDE.md
translated: true
type: note
---

Question: 如何让 Claude Code 遵循自定义规则——应该将它们添加到 CLAUDE.md 中还是使用 skills？

Answer:

很好的问题。Claude Code 有几种注入持久指令的机制。下面是全面分解：

---

## 1. `CLAUDE.md` — 主要方法

这是给 Claude Code 持久指令的 **最推荐和原生** 方式。

### 工作原理

- Claude Code 在每个会话开始时 **自动读取** `CLAUDE.md`
- 您可以在不同级别拥有多个 `CLAUDE.md` 文件

### 文件位置（按顺序全部读取）

| Location | Scope |
|---|---|
| `~/.claude/CLAUDE.md` | Global — applies to ALL projects |
| `<project-root>/CLAUDE.md` | Project-level — applies to this repo |
| `<subdir>/CLAUDE.md` | Subdirectory-level — applies when working in that folder |

### 示例 `~/.claude/CLAUDE.md` 用于您的格式规则

```markdown
## Response Format Rules

Always respond in this exact format:

**Question:** [rephrased and grammar-fixed user question]

**Answer:**
[full answer in clean Markdown, always in English]

**References:**
[only show if there is at least one, use bullet list with [url](url) format]

- No Grok render tags
- Do not show images, prefer text only
- Give comprehensive explanations for exam questions
- Always answer in English, even if the question is in Chinese
- Always search the web before answering
```

---

## 2. 项目级 `CLAUDE.md` — 用于团队/仓库规则

将 `CLAUDE.md` 放置在您的 **项目根目录** 中，用于特定于该代码库的规则：

```markdown
## Project Conventions
- Use TypeScript strict mode
- All functions must have JSDoc comments
- Run `npm test` before committing
```

这会进行版本控制，并自动与您的团队共享。

---

## 3. Skills (`/mnt/skills/`) — 用于 Claude.ai Web，不是 Claude Code

Skills（就像您在 **Claude.ai** 中看到的 `/mnt/skills/` 系统）是 **Claude.ai web 界面** 的功能，不是 Claude Code CLI。它们是由 Anthropic 平台注入的预加载指令文件。

**Claude Code 不支持 skills 系统。** 不要混淆两者。

---

## 4. 通过 API / `--system-prompt` 标志的系统提示

如果您以 **编程方式或通过 SDK** 调用 Claude Code，可以直接传递系统提示：

```bash
claude --system-prompt "Always answer in English. Follow this format: ..."
```

或在 SDK 中：

```javascript
const claude = new Anthropic();
// pass system prompt in your API call
```

---

## 5. `/memory` 命令（运行时）

在 Claude Code 会话中，您可以使用：

```
/memory
```

这允许您 **添加或编辑内存**，该内存会跨会话持久存在——类似于 CLAUDE.md，但通过交互方式管理。

---

## 最佳实践总结

| Goal | Method |
|---|---|
| Rules for ALL projects globally | `~/.claude/CLAUDE.md` |
| Rules for one specific project | `<project>/CLAUDE.md` |
| Rules for a subfolder | `<subdir>/CLAUDE.md` |
| One-off session rules | Type instructions inline or use `/memory` |
| Programmatic/API usage | `--system-prompt` flag or SDK system param |

---

## 针对您的用例的推荐

由于您的格式规则（仅英文、特定输出结构、始终搜索）是 **个人偏好**，应该处处适用，请将它们放入：

```
~/.claude/CLAUDE.md
```

这是 **全局 CLAUDE.md**，会自动应用于您使用 Claude Code 处理的每个项目——无需每个项目的设置。

References:

- [Claude Code – CLAUDE.md documentation](https://docs.claude.com/en/docs/claude-code/memory)
- [Claude Code overview](https://docs.claude.com/en/docs/claude-code/overview)
