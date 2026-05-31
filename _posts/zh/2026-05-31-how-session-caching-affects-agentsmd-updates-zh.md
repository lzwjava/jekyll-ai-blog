---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 会话缓存如何影响AGENTS.md更新
translated: true
type: note
---

以下是代码的完整说明：

AGENTS.md 作为系统提示的一部分加载，且系统提示**按会话缓存**——不会在每一轮重新构建。具体工作机制如下：

1. **新会话的第一轮** —— `agent/conversation_loop.py:288` 调用 `agent._build_system_prompt(system_message)`，进而触发 `agent/system_prompt.py:build_system_prompt_parts()`。该函数（第290-299行）从 `agent/prompt_builder.py:1468` 调用 `build_context_files_prompt()`，后者通过 `_load_agents_md()`（第1406-1419行）从磁盘读取 AGENTS.md。结果会缓存到 `agent._cached_system_prompt`。

2. **同一会话的后续轮次** —— `conversation_loop.py:582` 检查 `if agent._cached_system_prompt is None`。由于已设置，它会完全跳过重建过程，直接原样复用缓存的版本。这是有意为之——用于保持 Anthropic/OpenAI 前缀缓存的热度（文档见第571-581行）。

3. **会话恢复（网关路径）** —— 网关为每条消息创建一个新的 `AIAgent`。`conversation_loop.py:247-271` 从 SQLite 会话数据库加载存储的系统提示，而非重新构建。效果相同：不会读取 AGENTS.md 的变更。

4. **上下文压缩后** —— `conversation_compression.py:496` 设置一个新的 `_cached_system_prompt`，但它基于*现有*提示的结构重新构建，而非从磁盘读取。

5. **失效机制** —— `system_prompt.py:invalidate_system_prompt()`（第367-375行）将 `_cached_system_prompt` 设为 `None` 并从磁盘重新加载内存。但此函数仅在压缩事件后被调用，而不会在文件编辑后触发。

因此答案是：**你需要开始一个新会话**（例如，在 CLI 中使用 `/new`，或在网关中开始新对话）才能使 AGENTS.md 的变更生效。在同一会话内，系统提示会被冻结以保持前缀缓存的稳定性。无需重启 hermes 进程本身——只需开启一个新会话即可。

唯一例外：如果你在 CLI 中且会话从未被使用过（尚未有 `_cached_system_prompt`），那么第一条消息会读取到你的编辑内容。但一旦会话开始，提示就会被锁定。