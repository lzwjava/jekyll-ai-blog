---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Codex 中的 MCP 文件错误
translated: true
type: note
---

Question: 如何修复在 Codex 中调用 files.read_mcp_resource 时出现的 "unknown MCP server 'files'" 错误？

Answer: 

出现该错误的原因是 Codex (OpenAI 的 coding agent/CLI tool) 尝试使用 **MCP** (Model Context Protocol) 函数 `read_mcp_resource` (或类似的 `files.read_mcp_resource`) 来访问文件，但在你的环境中并没有实际配置或运行名为 `"files"` 的 **MCP server**。

MCP 是一种协议（最初由 Anthropic 发起，现在被包括 OpenAI Codex 在内的工具广泛采用），旨在让 AI agents 连接到外部 tools/services。Codex 内置的本地文件系统访问通常是通过直接的 file tools 或 shell commands 实现的，而**不是**通过名为 "files" 的 MCP server。

### 为什么会发生这种情况
Codex 的 model 有时会混淆普通的文件读取逻辑与基于 MCP 的读取逻辑（尤其是当它在 Cursor, Windsurf, Claude 等工具中见过大量 MCP 使用示例时）。这是 agent models 中已知的一种偶发行为 —— 即便不存在这样的 server，它也会产生幻觉 (hallucinates) 或过度泛化为 MCP 调用。

### 如何修复

1. **最常用且快速的解决方案**  
   直接在 **chat / prompt 中明确告诉 Codex** 停止在文件操作中使用 MCP：

   ```
   Do NOT use any MCP functions like read_mcp_resource, list_mcp_resources, files.read_mcp_resource etc. to read files.

   Use normal file reading methods instead:
   - Use shell tool to run cat, bat, head, etc.
   - Or use apply_patch / edit file tools when changing code
   - Or just read_file tool if available in this session
   ```

   然后重新发送你的原始请求。

2. **如果你确实想通过 MCP 访问文件系统（可选，高级选项）**  
   你可以实际设置一个本地文件系统 MCP server（存在多个社区版本），并将其命名为 `"files"`，这样调用就能生效：

   - 在 GitHub 上搜索 "filesystem MCP server" 或 "local files MCP Codex"
   - 常见的包括适配 Codex 的 ClaudeComputerCommander 风格 server，或者简单的基于 stdio 的 MCP servers
   - 将其添加到你的 Codex config（通常是 `~/.codex/config.toml` 或项目本地配置）中，例如：

     ```toml
     [mcp.servers.files]
     command = "npx @someorg/filesystem-mcp-server"
     # 或者
     command = "python /path/to/your/files-mcp-server.py"
     ```

   但在 95% 的情况下，这是**不需要的** —— 普通的 Codex file tools 已经足够了。

3. **其他常用的替代方法**
   - 重启 Codex CLI / VS Code extension
   - 运行 `/tools` 或 `codex /tools` 来查看当前实际可用的工具有哪些
   - 明确询问："list_mcp_resources" → 如果显示为空或没有 "files"，则证实了确实没有该 server
   - 暂时降级 model（如果正在使用 gpt-5-codex 等 preview models） —— 某些版本对 MCP 的幻觉更严重

简而言之：  
最彻底的修复方法通常是**在 prompt 中明确禁止 MCP file calls** —— Codex 非常擅长遵循此类指令。

References:  

- [Model sometimes tries to use MCP tool to read skills](https://github.com/openai/codex/issues/7639)
- [Codex not finding MCP servers](https://github.com/openai/codex/issues/6215)
- [Codex MCP client issues](https://github.com/openai/codex/issues/6465)
- [Codex System Prompt showing read_mcp_resource tool](https://gist.github.com/chigkim/ffed11a3e017d98698707dd24e78af51)