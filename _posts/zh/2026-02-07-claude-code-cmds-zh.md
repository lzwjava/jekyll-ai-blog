---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Claude Code 命令指南
translated: true
type: note
---

我将从 Anthropic 的文档中搜索有关 Claude Code 命令选项的最新信息。让我获取更多关于命令行选项的详细信息。根据文档，以下是关于 Claude Code 命令选项的全面介绍：

## Claude Code Command Options

### **Basic Commands**

**启动 Claude Code:**
- `claude` - 在当前目录启动交互式会话
- `claude "query"` - 运行单个查询并返回到 shell
- `claude -p "query"` - Print mode（非交互式，可用于脚本输出）

**会话管理:**
- `claude --continue` - 恢复最近的对话
- `claude -r "session-id" "query"` - 通过 ID 恢复特定会话
- `claude --resume` - 交互式菜单选择之前的会话
- `claude update` - 更新到最新版本
- `claude mcp` - 配置 Model Context Protocol servers

### **Key CLI Flags**

**工作目录:**
- `--add-dir <path> [<path2>...]` - 添加额外的目录供 Claude 访问
  ```bash
  claude --add-dir ../apps ../lib
  ```

**权限:**
- `--allowedTools` - 无需提示即可允许使用的工具
  ```bash
  claude --allowedTools "Bash(git log:*)" "Read"
  ```
- `--disallowedTools` - 无需提示即可拒绝的工具
- `--permission-mode <mode>` - 设置权限模式：`normal`、`auto-accept` 或 `plan`
  ```bash
  claude --permission-mode plan
  ```

**System Prompts (4 种选项):**
- `--system-prompt` - 完全控制，移除默认指令
- `--system-prompt-file <path>` - 从文件加载自定义 prompt
- `--append-system-prompt` - 在保留默认设置的同时添加指令（推荐）
- `--append-system-prompt-file <path>` - 在保留默认设置的同时从文件追加

**输出格式:**
- `-p, --print` - 非交互式 print mode
- `--output-format json` - 用于脚本/自动化的 JSON 输出
- `--verbose` - 详细日志

**Custom Agents:**
- `--agents <json>` - 定义自定义 subagents
  ```bash
  claude --agents '{
    "code-reviewer": {
      "description": "Expert code reviewer",
      "prompt": "Focus on code quality and security",
      "tools": ["Read", "Grep", "Glob", "Bash"],
      "model": "sonnet"
    }
  }'
  ```

### **Interactive Commands (Slash Commands)**

在 Claude Code 运行时可用：

**会话与配置:**
- `/help` - 显示可用命令
- `/config` - 打开设置界面
- `/login` - 切换账号
- `/vim` - 启用 vim 键绑定

**工作流:**
- `/resume` - 恢复之前的对话
- `/compact` - 压缩对话历史
- `/init` - 初始化新会话
- `/terminal-setup` - 为终端配置 Shift+Enter

**权限:**
- `/allowed-tools` - 配置工具权限

**Plugins & Extensions:**
- `/plugin` - 交互式管理插件
- `/hooks` - 查看/管理 hooks
- `/context` - 查看当前 context 使用情况

**自定义命令:**
你创建的任何技能都会变成一个 `/command` - 输入 `/` 即可查看所有可用命令

### **Plugin Commands (CLI)**

```bash
# 安装插件
claude plugin install <name>@<marketplace> [--scope user|project|local]

# 卸载插件
claude plugin uninstall <name>

# 启用/禁用
claude plugin enable <name>
claude plugin disable <name>

# 更新
claude plugin update <name>
```

### **Permission Modes**

会话期间使用 **Shift+Tab** 切换：
1. **Normal Mode** - Claude 对每个操作都会询问许可
2. **Auto-Accept Mode** (`⏵⏵`) - 自动接受文件编辑
3. **Plan Mode** (`⏵`) - Claude 仅进行只读操作的规划

### **Environment Variables**

- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` - 禁用后台任务
- `CLAUDE_CODE_TASK_LIST_ID=<name>` - 使用命名的任务列表
- `CLAUDE_CODE_ENABLE_TASKS=false` - 恢复到旧的 TODO 列表
- `MAX_THINKING_TOKENS` - 永久启用 extended thinking
- `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` - 每次命令后重置到项目目录
- `SLASH_COMMAND_TOOL_CHAR_BUDGET` - 调整技能字符预算

### **Interactive Features**

**输入:**
- `\` + Enter - 插入换行符
- Shift+Enter - 插入换行符（大多数终端）
- Ctrl+R - 反向搜索命令历史
- Tab - 切换 extended thinking 模式
- `!<command>` - 直接运行 bash 命令

**导航:**
- 方向键 - 命令历史
- Ctrl+O - 切换 verbose 模式

### **Common Workflow Examples**

```bash
# 在 plan mode 下探索代码库
claude --permission-mode plan "Analyze authentication system"

# 从之前的会话继续工作
claude --continue "Finish implementing OAuth"

# 脚本自动化
claude -p --output-format json "Run tests and report failures" | jq

# 从多个目录添加上下文
claude --add-dir ../shared ../config "Refactor API handlers"

# 给会话添加自定义指令
claude --append-system-prompt "Always write type-annotated Python"
```

有关任何特定功能的更多详细信息，你可以直接询问 Claude Code —— 它能够访问自己的文档并回答有关其功能的问题。
