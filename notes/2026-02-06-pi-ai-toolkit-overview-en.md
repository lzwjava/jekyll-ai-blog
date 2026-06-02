---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Pi AI Agent Toolkit Overview
translated: false
type: note
---

I'll fetch and analyze that GitHub repository for you.Let me fetch the detailed README and AGENTS documentation to give you a more comprehensive overview.# Pi Monorepo - Comprehensive Introduction

**Pi-mono** is an AI agent toolkit created by Mario Zechner (badlogic) that provides a complete ecosystem for building and deploying AI coding agents and managing LLM interactions. It's structured as a monorepo containing multiple interconnected packages.

## Core Philosophy

Pi takes a minimalist, extensible approach. Rather than shipping with every possible feature, it provides powerful defaults and lets you build what you need through skills, extensions, prompt templates, or third-party packages. The focus is on flexibility and real-world usability.

## Main Packages

### 1. **@mariozechner/pi-coding-agent** (The Flagship)

An interactive coding agent CLI that runs in your terminal. This is the main product most users interact with.

**Key Features:**

- Four operational modes: interactive chat, print/JSON output, RPC for process integration, and SDK for embedding
- Built-in tools: `read`, `write`, `edit`, and `bash` for file and system operations
- Multiple LLM provider support with automatic model cycling
- Session management with branching, forking, and tree navigation
- Extensible through skills (prompt enhancements), extensions (custom code), and packages

**Basic Usage:**

```bash
# Install
npm install -g @mariozechner/pi-coding-agent

# Interactive mode
pi "List all .ts files in src/"

# Non-interactive
pi -p "Summarize this codebase"

# Specify model
pi --provider openai --model gpt-4o "Help me refactor"

# Read-only mode
pi --tools read,grep,find,ls -p "Review the code"
```

### 2. **@mariozechner/pi-ai**

The foundational LLM toolkit providing a unified API across multiple providers.

**Supported Providers:**

- OpenAI (GPT-4, GPT-4o, o1, o3-mini)
- Anthropic (Claude Opus, Sonnet, Haiku)
- Google (Gemini)
- xAI (Grok)
- Mistral
- OpenRouter
- Azure OpenAI
- Any OpenAI-compatible API (Ollama, vLLM, LM Studio)

**Key Features:**

- Type-safe tool definitions using TypeBox schemas
- Streaming and completion APIs
- Built-in agent loop with automatic tool execution
- Tool argument validation
- Serializable conversation contexts

### 3. **@mariozechner/pi-agent**

Core agent runtime providing state management and tool execution orchestration.

**Capabilities:**

- Tool calling with validation
- State management across turns
- Event-driven architecture
- Integration with the pi-ai layer

### 4. **@mariozechner/pi-tui**

A terminal UI library with differential rendering for building responsive CLI interfaces.

**Features:**

- Efficient screen updates (only renders changes)
- Custom component system
- Input handling
- Used by the coding agent for its interactive interface

### 5. **@mariozechner/pi-web-ui**

Web components for building AI chat interfaces in browsers.

### 6. **@mariozechner/pi-mom**

A Slack bot that delegates messages to the pi coding agent, enabling team collaboration through Slack.

### 7. **@mariozechner/pi-proxy**

CORS proxy for making browser-based LLM API calls without exposing keys (though production apps should use proper backends).

### 8. **@mariozechner/pi** (pi-pods)

CLI tool for managing vLLM deployments on GPU pods, useful for self-hosting models.

## Extensibility System

### Skills

Prompt templates or instructions that enhance the agent's capabilities. They're loaded and injected into the system prompt.

### Extensions

TypeScript/JavaScript code that hooks into the agent's lifecycle through events:

- `session_start`, `session_switch`, `session_fork`
- `input`, `before_agent_start`, `agent_start`
- `turn_start`, `context`, `tool_call`, `tool_result`, `turn_end`
- `agent_end`, `session_compact`

Extensions can:

- Register custom commands (e.g., `/mycommand`)
- Add custom tools
- Intercept and modify messages
- Create UI widgets
- React to user input

### Pi Packages

Shareable bundles distributed via npm or git containing extensions, skills, prompts, and themes.

```bash
# Install from npm
pi install npm:@foo/pi-tools

# Install from git
pi install git:github.com/user/repo

# Local development
pi install /path/to/local/package
```

**Security Note:** Extensions run with full system permissions and can execute arbitrary code. Only install from trusted sources.

## Configuration & Customization

### Model Configuration

Add custom models via `~/.pi/agent/models.json`:

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [
        { "id": "llama3.1:8b" },
        { "id": "qwen2.5-coder:7b" }
      ]
    }
  }
}
```

### Authentication

Models require authentication via:

- Subscription login (`/login` command)
- API keys (environment variables or explicit configuration)

### Settings

Configure behavior through commands:

- `/settings` - Open settings UI
- `/model` or `Ctrl+L` - Select model
- `/tools` - Configure available tools
- `/theme` - Change appearance

### Environment Variables

- `PI_CODING_AGENT_DIR` - Config directory (default: `~/.pi/agent`)
- `PI_CACHE_RETENTION` - Cache strategy (`long` for extended, `short` for minimal)
- `PI_SKIP_VERSION_CHECK` - Skip startup version check
- `VISUAL` / `EDITOR` - External editor for `Ctrl+G`

## Development Workflow

The monorepo uses a lockstep versioning system where all packages maintain the same version number.

```bash
# Setup
npm install
npm run build

# Development
npm run dev              # Watch mode for all packages
./pi-test.sh            # Run from source

# Testing
./test.sh               # Non-LLM tests (no API keys needed)
npm test                # All tests

# Version management
npm run version:patch   # 0.7.5 → 0.7.6
npm run version:minor   # 0.7.5 → 0.8.0
npm run version:major   # 0.7.5 → 1.0.0

# Publishing
npm run publish         # Publish all packages to npm
```

## SDK Usage

Embed pi in your own applications:

```typescript
import { createPiSession } from '@mariozechner/pi-coding-agent';

const session = await createPiSession({
  cwd: process.cwd(),
  model: { provider: 'anthropic', id: 'claude-opus-4-5' }
});

// Send message and handle streaming
await session.sendMessage('Help me refactor this function', {
  onText: (text) => console.log(text),
  onToolCall: (tool) => console.log(`Using tool: ${tool.name}`)
});

// Interrupt or follow up
await session.steer('New instruction');
await session.followUp('After you\'re done, also do this');
```

## Platform Support

- **Windows**: Fully supported
- **Linux/macOS**: Native support
- **Termux (Android)**: Compatible
- Various terminal emulators with setup guides

## Real-World Usage

Pi is actively used in production environments. See [openclaw/openclaw](https://github.com/openclaw/openclaw) for a real-world SDK integration example.

## Community & Resources

- **License**: MIT
- **Stars**: 397+ on GitHub
- **Active Development**: Regular releases (currently v0.12.14)
- **Documentation**: Comprehensive docs in `/packages/coding-agent/docs/`
- **Discord**: Community discussions and package discovery

## Why Pi?

Pi stands out for its:

- **Unified API** across multiple LLM providers
- **Extensibility** through a well-designed plugin system
- **Terminal-first** approach with excellent TUI
- **Real agent capabilities** with proper tool execution
- **Production-ready** with SDK for embedding
- **Active maintenance** and growing ecosystem

Whether you need a powerful coding assistant, want to build custom AI tools, or manage LLM deployments, pi-mono provides the building blocks.
