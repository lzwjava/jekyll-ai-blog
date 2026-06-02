---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯 AGENTS.md 加载规则
translated: true
type: note
---

以下是 Hermes 加载每个项目的 AGENTS.md 的方式：

**入口点：**`agent/prompt_builder.py` 中的 `build_context_files_prompt()` （第 1412 行）

**优先级链（第一个匹配获胜——仅加载一个项目上下文类型）：**

1. `.hermes.md` / `HERMES.md` — 从 cwd 向上遍历至 git root
2. `AGENTS.md` / `agents.md` — 仅 cwd （不向上遍历）
3. `CLAUDE.md` / `claude.md` — 仅 cwd
4. `.cursorrules` + `.cursor/rules/*.mdc` — 仅 cwd

**AGENTS.md 具体工作方式（`_load_agents_md`，第 1350 行）：**

```python
def _load_agents_md(cwd_path: Path) -> str:
    for name in ["AGENTS.md", "agents.md"]:
        candidate = cwd_path / name
        if candidate.exists():
            content = candidate.read_text(encoding="utf-8").strip()
            content = _scan_context_content(content, name)  # 安全检查
            result = f"## {name}\n\n{content}"
            return _truncate_content(result, "AGENTS.md")  # 限制 20k 字符
    return ""
```

它只检查 cwd —— 不进行目录遍历。如果你在 `/Users/lzwjava/projects/hermes-agent` 中，它会查找该目录下的 `AGENTS.md`。

**与 `.hermes.md` 的关键区别：**`_find_hermes_md`（第 79 行）从 cwd 向上遍历父目录，直到达到 git root。因此，即使你在子目录中，也能找到仓库根目录下的 `.hermes.md`。

**集成到系统提示（`agent/system_prompt.py`，第 269 行）：**

```python
context_files_prompt = _r.build_context_files_prompt(...)
```

这会被前置到系统提示中，作为 `# Project Context`，并附注“以下项目上下文文件已加载，应被遵循。”

**安全性：**`_scan_context_content`（第 44 行）在注入前对内容进行威胁模式扫描。如果检测到提示注入模式，该文件会被阻止，并记录警告而非注入内容。

**截断：**`_truncate_content` 将每个上下文源限制在 20,000 字符以内。

**Cron 任务：**当 cron 任务设置了 `workdir` 时，`build_context_files_prompt()` 会以该目录作为 cwd 被调用，因此项目目录中的 AGENTS.md 会被注入到 cron 会话的系统提示中（参见 `cron/scheduler.py` 第 1648 行）。
