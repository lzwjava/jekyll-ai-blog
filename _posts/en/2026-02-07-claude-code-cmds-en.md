---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Claude Code Command Guide
translated: false
type: note
---

I'll search for the most current information about Claude Code's command options from Anthropic's documentation.Let me fetch more detailed information about the command-line options.Based on the documentation, here's a comprehensive introduction to Claude Code command options:

## Claude Code Command Options

### **Basic Commands**

**Starting Claude Code:**
- `claude` - Launch interactive session in current directory
- `claude "query"` - Run single query and return to shell
- `claude -p "query"` - Print mode (non-interactive, scriptable output)

**Session Management:**
- `claude --continue` - Resume most recent conversation
- `claude -r "session-id" "query"` - Resume specific session by ID
- `claude --resume` - Interactive menu to select previous session
- `claude update` - Update to latest version
- `claude mcp` - Configure Model Context Protocol servers

### **Key CLI Flags**

**Working Directories:**
- `--add-dir <path> [<path2>...]` - Add additional directories for Claude to access
  ```bash
  claude --add-dir ../apps ../lib
  ```

**Permissions:**
- `--allowedTools` - Tools allowed without prompting
  ```bash
  claude --allowedTools "Bash(git log:*)" "Read"
  ```
- `--disallowedTools` - Tools to deny without prompting
- `--permission-mode <mode>` - Set permission mode: `normal`, `auto-accept`, or `plan`
  ```bash
  claude --permission-mode plan
  ```

**System Prompts (4 options):**
- `--system-prompt` - Complete control, removes default instructions
- `--system-prompt-file <path>` - Load custom prompt from file
- `--append-system-prompt` - Add instructions while keeping defaults (recommended)
- `--append-system-prompt-file <path>` - Append from file while keeping defaults

**Output Formats:**
- `-p, --print` - Non-interactive print mode
- `--output-format json` - JSON output for scripting/automation
- `--verbose` - Detailed logging

**Custom Agents:**
- `--agents <json>` - Define custom subagents
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

Available when Claude Code is running:

**Session & Configuration:**
- `/help` - Show available commands
- `/config` - Open settings interface
- `/login` - Switch accounts
- `/vim` - Enable vim keybindings

**Workflow:**
- `/resume` - Resume previous conversation
- `/compact` - Compact conversation history
- `/init` - Initialize new session
- `/terminal-setup` - Configure Shift+Enter for terminal

**Permissions:**
- `/allowed-tools` - Configure tool permissions

**Plugins & Extensions:**
- `/plugin` - Manage plugins interactively
- `/hooks` - View/manage hooks
- `/context` - View current context usage

**Custom Commands:**
Any skill you create becomes a `/command` - type `/` to see all available

### **Plugin Commands (CLI)**

```bash
# Install plugin
claude plugin install <name>@<marketplace> [--scope user|project|local]

# Remove plugin
claude plugin uninstall <name>

# Enable/disable
claude plugin enable <name>
claude plugin disable <name>

# Update
claude plugin update <name>
```

### **Permission Modes**

Toggle with **Shift+Tab** during session:
1. **Normal Mode** - Claude asks permission for each action
2. **Auto-Accept Mode** (`⏵⏵`) - Automatically accept file edits
3. **Plan Mode** (`⏸`) - Claude plans with read-only operations

### **Environment Variables**

- `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` - Disable background tasks
- `CLAUDE_CODE_TASK_LIST_ID=<name>` - Use named task list
- `CLAUDE_CODE_ENABLE_TASKS=false` - Revert to old TODO list
- `MAX_THINKING_TOKENS` - Enable extended thinking permanently
- `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` - Reset to project dir after each command
- `SLASH_COMMAND_TOOL_CHAR_BUDGET` - Adjust skill character budget

### **Interactive Features**

**Input:**
- `\` + Enter - Insert newline
- Shift+Enter - Insert newline (most terminals)
- Ctrl+R - Reverse search command history
- Tab - Toggle extended thinking mode
- `!<command>` - Run bash command directly

**Navigation:**
- Arrow keys - Command history
- Ctrl+O - Toggle verbose mode

### **Common Workflow Examples**

```bash
# Explore codebase in plan mode
claude --permission-mode plan "Analyze authentication system"

# Continue work from previous session
claude --continue "Finish implementing OAuth"

# Script automation
claude -p --output-format json "Run tests and report failures" | jq

# Add context from multiple directories
claude --add-dir ../shared ../config "Refactor API handlers"

# Custom instructions for session
claude --append-system-prompt "Always write type-annotated Python"
```

For more details on any specific feature, you can ask Claude Code directly - it has access to its own documentation and can answer questions about its capabilities.
