---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 工作目录如何影响Hermes
translated: true
type: note
---

好问题。以下是工作目录实际影响 Hermes 的方式：

**机制：`TERMINAL_CWD`**

当你从一个目录启动 `hermes` 时，该目录就成为 `TERMINAL_CWD` —— 一个所有工具都会读取的环境变量。它是以下操作的基准：

1. **终端命令** —— `bash` 命令以 `cwd=TERMINAL_CWD` 运行（terminal_tool.py:1033）
2. **文件操作** —— `read_file`、`write_file`、`search_files` 根据它解析相对路径（file_tools.py:122-126）
3. **execute_code** —— Python 脚本默认在 `TERMINAL_CWD` 中运行（code_execution_tool.py:1230）
4. **上下文文件** —— 从 cwd 加载 AGENTS.md、CLAUDE.md、.cursorrules
5. **子代理委派** —— 子代理继承父代理的 cwd

**针对搜索/ grep 的具体影响：**

`search_files` 工具使用 ripgrep (`rg`)。当你传入相对路径（如 `.` 或 `src/`）时，它会根据 `TERMINAL_CWD` 解析；传入绝对路径时则直接搜索该路径。Ripgrep 非常快（比 grep 快约 10 倍），因此对于正常项目规模，目录大小几乎没有影响。一个 10 万文件的单体仓库仍然可以在毫秒级完成搜索。

**真正的影响在于：**

- **上下文加载** —— 这是最大的影响。如果你从 `/Users/lzwjava/projects/hermes-agent` 启动，它会加载该项目的 AGENTS.md；如果从 `~/projects/ww` 启动，则加载 ww 的上下文。不同的 cwd = 不同的系统提示上下文。
- **相对路径解析** —— 所有工具调用中的相对路径都从 cwd 解析。`read_file("src/foo.py")` 在不同目录下含义不同。
- **项目级虚拟环境** —— 在 `project` 模式下，`execute_code` 使用 cwd 中的虚拟环境，因此根据启动位置不同，你会获得不同的 Python 包。

**这会拖慢速度吗？**

对 grep/搜索速度没有实质性影响。Ripgrep 是 I/O 密集型的，且速度极快。唯一可能因 cwd 影响性能的场景是：你意外地从 `$HOME` 或 `/` 启动 —— 此时 `search_files` 使用相对路径可能会遍历整个文件系统。但那是用户错误，不是 Hermes 的设计问题。

**TL;DR：** Cwd 影响的是 Hermes 所使用的 *上下文和路径*，而不是 *运行速度*。从项目根目录启动即可，一切正常。
