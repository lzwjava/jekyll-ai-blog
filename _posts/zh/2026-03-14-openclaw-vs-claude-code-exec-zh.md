---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw VS Claude 代码执行工具
translated: true
type: note
---

**问题：** OpenClaw 是如何实现其 `exec` 工具来执行 shell 命令的，以及 Claude Code 的 Bash 工具与上面所示的简单 `subprocess.run` 模式相比如何？

**回答：**

## 比较：您的简单 `exec_command` 与 OpenClaw 与 Claude Code

---

### 1. 您的实现（基准）

您的代码是最简单的模式：

```python
result = subprocess.run(
    command, shell=True, capture_output=True, text=True, timeout=30
)
```

关键特性：
- **无状态**：每次调用都会启动一个新的 shell —— 调用之间不共享状态（环境变量、`cd`）
- **立即执行**：使用 `shell=True`，意味着 OS shell 解释字符串
- **仅同步**：阻塞直到完成或 30s 超时
- **无安全层**：任何命令无审批即可运行

---

### 2. OpenClaw 的 `exec` 工具

OpenClaw 的设计远更复杂。主要差异：

#### 执行目标（`host` 参数）
OpenClaw 通过 `host` 参数支持多种执行目标：`sandbox`（默认，在容器内使用 `sh -lc` 登录 shell 运行）、`gateway`（在主机上运行）或 `node`（配对的远程设备）。每个都有自己的安全执行模式。

#### 前台 + 后台执行
OpenClaw 通过 `process` 工具支持前台和后台执行。后台执行时，它立即返回 `status: "running"` 和 `sessionId`，您可以使用 `process` 来轮询、日志、写入、杀死或清除后台会话。

#### PTY（伪终端）支持
OpenClaw 支持 `pty: true` 参数，用于在伪终端中运行命令，这对于仅 TTY CLI 和仅在 stdout 为真实终端时才产生输出的终端 UI 很有用。

#### Shell 检测
在非 Windows 主机上，OpenClaw 使用 `SHELL` 环境变量，但如果 shell 是 `fish`，则优先使用 PATH 中的 `bash`（或 `sh`）以避免 fish 不兼容的脚本。在 Windows 上，它优先使用 PowerShell 7，回退到 PowerShell 5.1。

#### 安全与审批系统
OpenClaw 在 gateway 或 node 主机上执行前有每个请求的审批系统。当需要审批时，exec 工具立即返回 `status: "approval-pending"` 和审批 ID。一旦审批通过（或拒绝/超时），Gateway 会发出系统事件。

当 `security=allowlist` 时，shell 命令仅在每个管道段都列入允许列表时才自动允许。在 allowlist 模式下，连锁（`;`、`&&`、`||`）和重定向会被拒绝，除非每个顶级段都满足允许列表。

#### 环境与 PATH 保护
主机执行拒绝 `env.PATH` 和加载器覆盖（`LD_*/DYLD_*`）以防止二进制劫持或注入代码。OpenClaw 在生成的命令环境中设置 `OPENCLAW_SHELL=exec`，以便 shell/profile 规则检测 exec-tool 上下文。

#### 大致内部结构（概念性）：

```
exec(command, host, security, pty, background, yieldMs, env, elevated)
 → 路由至：sandbox 容器 | gateway 主机 | 远程 node
 → 应用安全策略：deny | allowlist | full
 → 检查审批关卡 (exec-approvals.json)
 → 生成：sh -lc / bash / pwsh（如果请求则带 PTY）
 → 如果后台：返回 sessionId，通过 process 工具跟踪
 → 如果前台：流式/捕获输出 → 返回结果
```

---

### 3. Claude Code 的 Bash 工具

Claude Code 使用**持久 bash 会话**——与您的单次 `subprocess.run` 根本不同。

Bash 工具使 Claude 能够在**持久 bash 会话**中执行 shell 命令，允许环境变量和工作目录在命令间持久化。它实现为无 schema 工具——schema 内置于 Claude 模型中，开发者无法修改。

官方参考实现：

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

会话状态在调用间保持——如 `cd /tmp` 等命令会为后续命令持久化。它还支持 `restart` 输入来重置会话。

Claude Code 的 Bash 工具捕获最多 30,000 字符输出，默认超时 2 分钟（可配置至 10 分钟）。它还支持 `PreToolUse` 和 `PostToolUse` 钩子用于审计日志和安全防护。

---

### 总结比较表

| 特性 | 您的 `exec_command` | OpenClaw `exec` | Claude Code `bash` |
|---|---|---|---|
| **会话状态** | ❌ 每次新 shell | ❌（每次调用） | ✅ 持久 bash |
| **后台执行** | ❌ | ✅（带 sessionId） | ✅（Ctrl+B 或请求） |
| **PTY 支持** | ❌ | ✅ `pty: true` | ❌（功能请求） |
| **审批关卡** | ❌ | ✅ 每个命令 | ✅ 每个命令提示 |
| **沙箱化** | ❌ | ✅ 容器/node | ❌（主机运行） |
| **Shell 选择** | OS 默认 | fish→bash 回退 | `/bin/bash` 硬编码 |
| **安全策略** | ❌ | allowlist/deny/full | 基于钩子的防护 |
| **超时** | 30s 固定 | 可配置 | 2 分钟（至 10） |

关键架构差异是：**您的代码和 OpenClaw** 是**每次调用无状态**的工具，而 **Claude Code 的 bash 是状态化的**——它在会话中的多个工具调用间保持单个长期运行的 bash 进程。
