---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes代理的自定义指令
translated: true
type: note
---

**问题：** 如何为 hermes-agent 添加自定义指令或系统消息？

**回答：**

Hermes 提供了**三种不同的机制**来注入自定义指令，每种机制的作用范围不同：

---

## 1. `~/.hermes/SOUL.md` — 全局个性/系统提示

这是**实例级别的系统消息**，最接近自定义系统提示。

```bash
# 直接编辑
nano ~/.hermes/SOUL.md
```

示例内容：
```markdown
# Soul
你是一名资深 AI 工程师。请简洁直接。
除非被要求，否则避免冗长的解释。
优先使用 Python、CLI 工具和第一性原理推理。
绝不建议 GUI 工作流。
始终考虑边界情况和错误处理。
```

Hermes 会自动生成初始 SOUL 文件，并使用 `~/.hermes/SOUL.md` 作为实例级别的个性来源，全局注入到每个会话中。

---

## 2. `AGENTS.md` — 项目级指令

在项目**根目录**下放置一个 `AGENTS.md` 文件，它会自动注入到每个会话中——配置后无需额外操作。

```bash
# 在仓库根目录下
cat > AGENTS.md << 'EOF'
# 项目上下文
- 基于 FastAPI 后端，使用 SQLAlchemy ORM
- 数据库操作始终使用 async/await
- 测试放在 tests/ 目录，使用 pytest-asyncio
- 绝不提交 .env 文件
- 优先使用 uv 而非 pip
EOF
```

如果你已经有 `.cursorrules` 或 `.cursor/rules/*.mdc` 文件，Hermes 也会读取它们——无需重复编写编码规范。

---

## 3. 通过 `/skills` 使用技能——可复用的提示注入

技能斜杠命令由 `agent/skill_commands.py` 处理，它会扫描 `~/.hermes/skills/` 目录，并将技能作为用户消息（而非系统提示）注入，以保留提示缓存。

```bash
# 列出可用技能
/skills

# 直接调用技能
/github-pr-workflow
```

你可以编写自己的技能文件：
```bash
mkdir -p ~/.hermes/skills
cat > ~/.hermes/skills/my-style.md << 'EOF'
# my-style
始终先给出代码，再给出解释。
所有 Python 代码必须使用类型注解。
EOF
```

---

## 决策矩阵

| 使用场景 | 机制 |
|---|---|
| 持久的个性/语气 | `~/.hermes/SOUL.md` |
| 项目特定的规范 | 仓库根目录下的 `AGENTS.md` |
| 可复用的按需工作流 | `~/.hermes/skills/*.md` |
| 一次性会话指令 | 直接在聊天中输入 |

---

## 关键注意事项

记忆是冻结的快照——会话期间所做的更改不会出现在系统提示中，直到下一个会话开始。代理会立即写入磁盘，但提示缓存在会话中不会失效。

系统提示应该定义**稳定行为**——语气、安全边界、工具使用规范。它不应成为存放秘密、项目运行手册、临时上下文或所有偏好的垃圾场。

对你来说：将你“简洁、代码优先、AI 原生、无 GUI”的偏好一次性写入 `SOUL.md`，然后忘记它。

**参考链接：**

- [技巧与最佳实践 — Hermes Agent 文档](https://hermes-agent.nousresearch.com/docs/guides/tips)
- [将 SOUL.md 与 Hermes 配合使用](https://hermes-agent.nousresearch.com/docs/guides/use-soul-with-hermes)
- [AGENTS.md — NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md)
