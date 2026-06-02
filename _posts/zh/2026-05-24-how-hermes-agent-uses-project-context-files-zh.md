---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes Agent 如何使用项目上下文文件
translated: true
type: note
---

现在我有了清晰的了解。以下是 AGENTS.md 在 hermes-agent 中按项目规则工作的方式：

---

## AGENTS.md 在 Hermes Agent 中的工作方式

共有两个注入点用于加载项目级上下文文件：

### 1. 启动时：系统提示注入

当你在某个目录中启动 `hermes` 时，`agent/prompt_builder.py::build_context_files_prompt()` 会在启动时运行。它会扫描当前工作目录，按优先级顺序查找项目上下文文件（最先找到的生效）：

    1. .hermes.md / HERMES.md  （向上遍历至 git 根目录）
    2. AGENTS.md / agents.md   （仅当前工作目录）
    3. CLAUDE.md / claude.md   （仅当前工作目录）
    4. .cursorrules             （仅当前工作目录）

其中**只有一份**文件会被加载到系统提示中（上限为 20,000 字符）。找到的内容会被包裹上标题 `# Project Context — The following project context files have been loaded and should be followed`，并注入到系统提示的 `context` 插槽中。

与此独立的是，`~/.hermes/SOUL.md`（你的全局身份/人格）始终被单独加载到 `stable` 插槽中。

### 2. 运行时：子目录提示发现

这是最巧妙的部分。`agent/subdirectory_hints.py` 实现了一个 `SubdirectoryHintTracker`，它会监控工具调用过程。当 agent 进入某个子目录时（通过 `read_file`、`terminal`、`search_files` 等工具），跟踪器会：

1. 从工具参数中提取目标目录
2. 向上遍历最多 5 层父目录，查找 AGENTS.md / CLAUDE.md / .cursorrules
3. 首次访问某个目录时，加载找到的任何提示文件（每个上限为 8,000 字符）
4. 将提示文本追加到工具结果中——**而不是系统提示**中

这意味着：如果 `project/AGENTS.md` 包含顶层规则，而 `project/backend/AGENTS.md` 包含后端特定规则，那么当 agent 开始在 `backend/` 目录中工作时，会立即获得后端规则——而无需修改系统提示（从而保留提示缓存）。

### 如何使用

在你的项目根目录中放置一个 `AGENTS.md` 文件。以 hermes-agent 自身为例（就是你正在看的这个）：

    hermes-agent/AGENTS.md   ← 项目级规则

通常包含的内容：
- 开发环境设置（虚拟环境、依赖）
- 项目结构概述
- 如何添加工具/命令
- 测试约定
- 提交约定
- 关键架构决策

### --ignore-rules 标志

如果你想跳过所有上下文文件加载（例如用于批量处理、数据生成等）：

    hermes --ignore-rules
    # 或者：HERMES_IGNORE_RULES=1 hermes

这会在 AIAgent 上设置 `skip_context_files=True` 和 `skip_memory=True`。

### 流程总结

    会话开始：
      CWD/AGENTS.md → 系统提示的 "context" 插槽（仅启动时一次）
      ~/.hermes/SOUL.md → 系统提示的 "stable" 插槽（始终加载）

    对话过程中：
      Agent 调用 read_file("backend/src/main.py")
        → 跟踪器发现 "backend/src/" 是新的
        → 扫描 backend/src/、backend/、项目根目录查找提示文件
        → 将找到的任何 AGENTS.md 内容追加到工具结果中
        → 将该目录标记为已加载（不会重复加载）

此设计在保留提示缓存（系统提示在对话过程中不改变）的同时，仍能在需要时向 agent 提供项目特定的上下文。
