---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix MCP Files Error in Codex
translated: false
type: note
---

Question: How to fix the error "unknown MCP server 'files'" when calling files.read_mcp_resource in Codex?

Answer:

The error occurs because Codex (OpenAI's coding agent/CLI tool) is trying to use the **MCP** (Model Context Protocol) function `read_mcp_resource` (or similar: `files.read_mcp_resource`) to access a file, but there is **no MCP server** actually named `"files"` configured or running in your environment.

MCP is a protocol (originally from Anthropic, now adopted widely including by OpenAI Codex) that lets AI agents connect to external tools/services. The built-in local filesystem access in Codex usually happens via direct file tools or shell commands — **not** via an MCP server called "files".

### Why this happens
Codex's model sometimes confuses normal file reading with MCP-based reading (especially when it has seen many examples of MCP usage in Cursor, Windsurf, Claude, etc.). This is a known occasional behavior in agent models — it hallucinates or over-generalizes to an MCP call even when no such server exists.

### How to fix it

1. **Most common & quick solution**
   Just **tell Codex explicitly in the chat / prompt** to stop using MCP for file operations:

   ```
   Do NOT use any MCP functions like read_mcp_resource, list_mcp_resources, files.read_mcp_resource etc. to read files.

   Use normal file reading methods instead:
   - Use shell tool to run cat, bat, head, etc.
   - Or use apply_patch / edit file tools when changing code
   - Or just read_file tool if available in this session
   ```

   Then re-ask your original request.

2. **If you want real filesystem access via MCP (optional, advanced)**
   You can actually set up a local filesystem MCP server (several community ones exist), and name it `"files"` so the call would work:

   - Search GitHub for "filesystem MCP server" or "local files MCP Codex"
   - Popular ones include things like ClaudeComputerCommander style servers adapted for Codex, or simple stdio-based MCP servers
   - Add it to your Codex config (usually `~/.codex/config.toml` or project-local config) like:

     ```toml
     [mcp.servers.files]
     command = "npx @someorg/filesystem-mcp-server"
     # or
     command = "python /path/to/your/files-mcp-server.py"
     ```

   But in 95% of cases this is **not needed** — normal Codex file tools are enough.

3. **Other workarounds people use**
   - Restart Codex CLI / VS Code extension
   - Run `/tools` or `codex /tools` to see what is actually available
   - Explicitly ask: "list_mcp_resources" → if it shows empty or no "files", that's confirmation there is no such server
   - Downgrade model temporarily (if using preview models like gpt-5-codex) — some versions hallucinate MCP more

In short:
The cleanest fix is usually **explicitly forbidding MCP file calls in your prompt** — Codex listens very well to such instructions.

References:

- [Model sometimes tries to use MCP tool to read skills](https://github.com/openai/codex/issues/7639)
- [Codex not finding MCP servers](https://github.com/openai/codex/issues/6215)
- [Codex MCP client issues](https://github.com/openai/codex/issues/6465)
- [Codex System Prompt showing read_mcp_resource tool](https://gist.github.com/chigkim/ffed11a3e017d98698707dd24e78af51)
