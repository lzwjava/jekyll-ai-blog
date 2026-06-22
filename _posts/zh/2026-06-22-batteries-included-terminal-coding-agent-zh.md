---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 包含电池的终端编码代理
translated: true
type: note
---

**问题：** omp.sh 是什么？

**回答：**

`omp`（Oh My Pi）是一个**开箱即用的终端编码代理**——可以理解为 Claude Code，但在工具链层面集成了真正的 IDE。它是 [Mario Zechner 的 Pi](https://github.com/badlogic/pi) 的一个分支，由 [Can Bölük (can1357)](https://github.com/can1357) 进行了大量扩展。

该项目在数月内飙升至 5500+ 星标，拥有 458 个分支的生态系统——这表明团队需要的是生产级工具，而非演示级提示词。（截至目前，有消息称星标已接近 13.6k，增长迅猛。）

---

## 它与 Claude Code / Cursor 有何不同

大多数代理工具链给模型提供的是 Python 沙箱、`str_replace` 和一些 grep 功能。omp 的核心观点是：**瓶颈在于工具链，而非模型。** 它在架构层面解决了五种常见的失败模式：

### 1. 哈希锚定编辑（hashline）
每一行都携带一个简短的基于内容哈希的锚点。模型通过锚点进行编辑，无需重新生成空白字符；过时的锚点会在文件损坏前被捕获。这消除了困扰大多数 `str_replace` 式代理的空白/缩进之争。数据令人瞩目：Grok Code Fast 的编辑成功率从 6.7% 跃升至 68.3%——一旦编辑格式不再消耗模型，成功率提升了十倍。Grok 4 Fast 的输出 token 减少了 61%，因为针对错误差异的重试循环消失了。

### 2. 真正的 LSP 集成（不仅仅是 grep）
请求重命名就能得到重命名。调用会经过 `workspace/willRenameFiles`，因此重新导出、桶文件（barrel files）和别名导入都会在文件移动前更新。你的 IDE 知道的一切，代理也知道。

### 3. 真正的 DAP 调试（不仅仅是打印语句）
C 二进制程序段错误：代理会连接 lldb，步进到坏指针处，读取栈帧。Go 服务挂起：它连接 dlv 并遍历 goroutine。Python 进程卡死：debugpy，暂停，检查，求值。内置适配器：gdb、lldb-dap、debugpy、dlv、js-debug-adapter。

### 4. 原生 Rust 核心（热路径上无 fork/exec）
约 2.7 万行 Rust 代码分布在三个 crate 中：`pi-natives`、`pi-shell`、`pi-ast`。搜索、shell、AST、高亮、PTY、图片解码、BPE 计数——全部在 libuv 线程池中就地完成。其他代理会调用外部 `rg`、`grep`、`find`——每次调用都是一次 fork/exec 往返。omp 则将真正的实现链接到进程内部。

### 5. 子代理 + IRC 总线
它会生成子代理，子代理通过进程内的 IRC 总线进行协调。`task` 工具会并行派生子代理，并可选择性地隔离工作空间。`/collab` 会将会话实时推送到中继，并分享一个链接用于结对调试。

---

## 规模
**40+ 提供商 · 32 个内置工具 · 13 个 LSP 操作 · 27 个 DAP 操作 · 约 2.7 万行 Rust 核心代码。**

提供商包括：通过 OAuth 接入 Claude Pro/Max、ChatGPT、Copilot、Cursor、Z.AI 等；或者将 API 密钥放入环境变量。按角色设定的模型（默认、轻量、慢速、规划）会根据你的认证信息自动解析。

---

## 技术栈

- **运行时**：Bun（TypeScript 包）+ Rust N-API 插件
- **包名**：`@oh-my-pi/pi-coding-agent`
- **配置**：`~/.omp/agent/`——会话存储为 JSONL，配置文件为 `config.yml`
- **会话**：支持恢复、分支、派生、共享

---

## 安装

```bash
npm install -g @oh-my-pi/pi-coding-agent
# 或通过 bun
bun install -g @oh-my-pi/pi-coding-agent
```

---

## 对你的关联性

鉴于你正在构建 CLI 代理（`ww`、`iclaw`、`zz`）并且使用 Zed——值得注意：在 Zed 内部运行 omp，你就能获得与终端驱动时相同的代理——读取你当前正在查看的缓冲区，通过编辑器的保存路径写入内容，在编辑器的终端中生成 shell。

此外：omp 会读取磁盘上已有的八种代理规则文件，且保持其原始格式——Cursor MDC、Cline `.clinerules`、Codex `AGENTS.md`、Copilot `applyTo` 等。无需迁移脚本。

如果你正在考虑构建自己的代理工具链，这种 Rust 原生的代理工具方法（进程内 grep、AST、BPE 计数）在架构上非常有趣——该代码库值得一读。

**参考链接：**

- [omp.sh](https://omp.sh)
- [github.com/can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)
- [agentpedia.codes — Oh My Pi 深入解读](https://agentpedia.codes/blog/oh-my-pi-terminal-coding-agent-guide)
- [explainx.ai — omp vs Claude Code](https://explainx.ai/blog/oh-my-pi-terminal-coding-agent-omp-mario-zechner-2026)