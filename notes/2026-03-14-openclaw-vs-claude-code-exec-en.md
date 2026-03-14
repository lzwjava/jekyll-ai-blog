---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw vs Claude Code Exec Tools
translated: false
type: note
---

**Question:** How does OpenClaw implement its `exec` tool for shell command execution, and how does Claude Code's Bash tool compare to the simple `subprocess.run` pattern shown above?

**Answer:**

## Comparison: Your Simple `exec_command` vs OpenClaw vs Claude Code

---

### 1. Your Implementation (Baseline)

Your code is the simplest possible pattern:

```python
result = subprocess.run(
    command, shell=True, capture_output=True, text=True, timeout=30
)
```

Key characteristics:
- **Stateless**: each call spawns a new shell — no state (env vars, `cd`) is shared between calls
- **Fire-and-forget**: uses `shell=True`, meaning the OS shell interprets the string
- **Synchronous only**: blocks until completion or 30s timeout
- **No security layer**: any command runs without approval

---

### 2. OpenClaw's `exec` Tool

OpenClaw's design is far more sophisticated. Key differences:

#### Execution Targets (`host` parameter)
OpenClaw supports multiple execution targets via the `host` parameter: `sandbox` (default, runs inside a container using `sh -lc` login shell), `gateway` (runs on the host machine), or `node` (a paired remote device). Each has its own security enforcement mode.

#### Foreground + Background Execution
OpenClaw supports both foreground and background execution via the `process` tool. When backgrounded, it returns `status: "running"` with a `sessionId` immediately, and you can use `process` to poll, log, write, kill, or clear background sessions.

#### PTY (Pseudo-Terminal) Support
OpenClaw supports a `pty: true` parameter for running commands in a pseudo-terminal, useful for TTY-only CLIs and terminal UIs that only produce output when stdout is a real terminal.

#### Shell Detection
On non-Windows hosts, OpenClaw uses the `SHELL` environment variable, but if the shell is `fish`, it prefers `bash` (or `sh`) from PATH to avoid fish-incompatible scripts. On Windows, it prefers PowerShell 7, falling back to PowerShell 5.1.

#### Security & Approval System
OpenClaw has a per-request approval system before exec runs on gateway or node hosts. When approvals are required, the exec tool returns immediately with `status: "approval-pending"` and an approval ID. Once approved (or denied/timed out), the Gateway emits system events.

When `security=allowlist`, shell commands are auto-allowed only if every pipeline segment is allowlisted. Chaining (`;`, `&&`, `||`) and redirections are rejected in allowlist mode unless every top-level segment satisfies the allowlist.

#### Environment & PATH Protection
Host execution rejects `env.PATH` and loader overrides (`LD_*/DYLD_*`) to prevent binary hijacking or injected code. OpenClaw sets `OPENCLAW_SHELL=exec` in the spawned command environment so shell/profile rules can detect the exec-tool context.

#### Approximate internal structure (conceptual):

```
exec(command, host, security, pty, background, yieldMs, env, elevated)
 → route to: sandbox container | gateway host | remote node
 → apply security policy: deny | allowlist | full
 → check approval gates (exec-approvals.json)
 → spawn: sh -lc / bash / pwsh (with PTY if requested)
 → if background: return sessionId, track via process tool
 → if foreground: stream/capture output → return result
```

---

### 3. Claude Code's Bash Tool

Claude Code uses a **persistent bash session** — fundamentally different from your one-shot `subprocess.run`.

The bash tool enables Claude to execute shell commands in a **persistent bash session**, allowing environment variables and working directory to persist across commands. It is implemented as a schema-less tool — the schema is built into Claude's model and cannot be modified by the developer.

The official reference implementation:

```python
class BashSession:
    def __init__(self):
        self.process = subprocess.Popen(
            ["/bin/bash"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0,
        )
        self.output_queue = queue.Queue()
        self._start_readers() # background threads drain stdout/stderr

    def execute_command(self, command):
        self.process.stdin.write(command + "\n")
        self.process.stdin.flush()
        return self._read_output(timeout=10)
```

Session state is maintained across calls — commands like `cd /tmp` persist for subsequent commands. It also supports a `restart` input to reset the session.

Claude Code's Bash tool captures up to 30,000 characters of output and has a default timeout of 2 minutes (configurable up to 10). It also supports `PreToolUse` and `PostToolUse` hooks for audit logging and security guards.

---

### Summary Comparison Table

| Feature | Your `exec_command` | OpenClaw `exec` | Claude Code `bash` |
|---|---|---|---|
| **Session state** | ❌ New shell each call | ❌ (per invocation) | ✅ Persistent bash |
| **Background exec** | ❌ | ✅ (with sessionId) | ✅ (Ctrl+B or ask) |
| **PTY support** | ❌ | ✅ `pty: true` | ❌ (feature request) |
| **Approval gates** | ❌ | ✅ per-command | ✅ per-command prompt |
| **Sandboxing** | ❌ | ✅ container/node | ❌ (runs on host) |
| **Shell selection** | OS default | fish→bash fallback | `/bin/bash` hardcoded |
| **Security policy** | ❌ | allowlist/deny/full | hook-based guards |
| **Timeout** | 30s fixed | configurable | 2 min (up to 10) |

The key architectural difference is: **your code and OpenClaw** are **stateless per-invocation** tools, while **Claude Code's bash is stateful** — it keeps a single long-running bash process alive across multiple tool calls in a session.
