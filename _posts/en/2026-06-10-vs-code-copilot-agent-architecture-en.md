---
audio: false
generated: true
image: false
lang: en
layout: post
title: VS Code Copilot Agent Architecture
translated: false
type: note
---

Here's what I found. The VS Code codebase has a very extensive Copilot agent system. Here's the breakdown:

== COPILOT AGENT ARCHITECTURE ==

1. THREE CORE AGENT MODES (registered in promptFileContrib.ts)

   - Plan Agent (planAgentProvider.ts)
     - Read-only planning agent, NEVER implements
     - Workflow: Discovery → Alignment → Design → Refinement
     - Uses Explore/SearchSubagent for codebase research
     - Saves plans to /memories/session/plan.md via vscode/memory tool
     - Can hand off to implementation agent via handoff buttons
     - Tools: DEFAULT_READ_TOOLS (search, read, web, memory, github/issue_read, terminal output, test failures)
     - Config: chat.planAgent.model, chat.planAgent.additionalTools

   - Ask Agent (askAgentProvider.ts)
     - Read-only Q&A agent, strictly never modifies workspace
     - Workflow: Understand → Research → Clarify → Answer
     - Tools: DEFAULT_READ_TOOLS + mermaid diagram rendering + askQuestions
     - Config: chat.askAgent.model, chat.askAgent.additionalTools

   - Agent Mode (agentIntent.ts) — the main coding agent
     - Full read-write access, tool calling loop
     - Config: chat.agent.maxRequests (default 200)

2. AGENT HANDOFF SYSTEM (agentTypes.ts)

   AgentHandoff interface enables Plan → Agent transitions:
   - label, agent name, prompt, send flag, model override
   - buildAgentMarkdown() generates .agent.md YAML frontmatter dynamically
   - Handoff buttons rendered in chat UI for user to approve

3. SWITCH AGENT TOOL (switchAgentTool.ts)

   - ToolName.SwitchAgent — lets the main agent switch to Plan agent
   - Only supports switching TO Plan (not Ask or others)
   - Executes `workbench.action.chat.toggleAgentMode` command
   - Returns the Plan agent body as context after switch

4. TOOL CALLING LOOP (toolCallingLoop.ts — 2073 lines)

   The core agentic execution engine:
   - Iterative loop: build prompt → fetch LLM → execute tool calls → repeat
   - Tool call limit with configurable behavior (Confirm or Stop)
   - Start/Stop hooks for session lifecycle
   - Subagent start/stop hooks for nested agent tracking
   - Keep-alive probes during long builds (4 min interval)
   - Context overflow handling with retry at 0.5x safety factor
   - Supports yield requests from VS Code editor

5. SUBAGENT SYSTEM

   - SearchSubagentTool (searchSubagentTool.ts)
     - Runs a nested ToolCallingLoop for codebase research
     - Thoroughness levels: normal (1x) or deep (2x turn limit)
     - Returns synthesized search results to parent agent

   - ExecutionSubagentTool (executionSubagentTool.ts)
     - Runs terminal commands in a nested loop
     - Captures output, links trajectory back to parent session
     - Uses CapturingToken for OTel trace hierarchy

   - Explore Agent (ExploreAgentProvider)
     - Feature-flagged (ConfigKey.ExploreAgentEnabled)
     - Dedicated research subagent for the Plan agent

6. MODEL-SPECIFIC PROMPT SYSTEM (promptRegistry.ts)

   Each model family gets its own prompt template:
   - GPT-5 family: gpt5Prompt.tsx (305 lines)
     - CoreManageTodoList tool for plans
     - Detailed planning guidance with examples
     - Progress updates, preamble messages, final answer formatting
   - GPT-5.1 Codex: gpt51CodexPrompt.tsx (Codex CLI inspired)
   - GPT-5.5: gpt55BasePrompt.tsx (vivid personality, epistemically curious)
   - Anthropic/Claude: anthropicPrompts.tsx (706 lines)
     - Tool search with deferred tools
     - Codesearch mode instructions
   - xAI/Grok: xAIPrompts.tsx
   - ZAI: zaiPrompts.tsx

7. BACKGROUND TODO AGENT (backgroundTodoAgent/)

   A background LLM that maintains a todo list without blocking the main agent:
   - Runs in a queue, processes after each main agent round
   - Only updates when the list would actually change
   - Tracks: not-started, in-progress, completed states
   - Rules: never creates single-item lists, max 5 items, 3-8 word titles
   - Evidence-based completion (edits/files, not exploration)

8. CLAUDE CODE INTEGRATION (chatSessions/claude/)

   Full Claude Agent SDK integration:
   - ClaudeAgentManager manages lifecycle
   - ClaudeCodeSession wraps @anthropic-ai/claude-agent-sdk
   - Slash commands wizard for creating/managing subagents
   - Tool hooks for pre/post tool use
   - Session persistence via .jsonl files

9. CLOUD AGENT (cloudAgentBackend.ts)

   Delegates tasks to GitHub's cloud coding agents:
   - Jobs API (PR-based) and Task API (task-based) backends
   - Creates branches, implements changes, opens PRs
   - Real-time progress streaming in VS Code chat

10. CONFIGURATION KEYS (configurationService.ts)

    Key settings:
    - chat.agent.maxRequests (default 200)
    - chat.advanced.enableAskAgent (experiment-based)
    - chat.planAgent.model / chat.planAgent.additionalTools
    - chat.askAgent.model / chat.askAgent.additionalTools
    - chat.planAgent.defaultModel
    - chat.advanced.enableSwitchAgent (experiment-based)
    - ConfigKey.ExploreAgentEnabled
    - ConfigKey.Advanced.SearchSubagentToolEnabled
    - ConfigKey.Advanced.ExecutionSubagentToolCallLimit

11. PROMPT STRUCTURE (agentPrompt.tsx — 958 lines)

    The main AgentPrompt element:
    - System message with copilot identity, safety rules
    - Tool preamble instructions
    - Planning guidance (when to use plans, examples)
    - Task execution rules
    - Testing philosophy
    - Progress update cadence
    - Final answer formatting rules
    - SummarizedConversationHistory for long conversations
    - Cache breakpoints for Anthropic/OpenAI caching
    - Codesearch mode variant (agentic Ask)

12. INTENT SYSTEM (constants.ts)

    Intent enum includes:
    - AskAgent = 'askAgent'
    - Agent (main coding agent)
    - EditCode, InlineChat, etc.

13. AGENT INSTRUCTIONS LOCATOR (agentInstructionsLocator.ts)

    Discovers .github/copilot-instructions.md and agent-specific instructions
    from the workspace for customizing agent behavior.

== KEY FILES ==

Core agent logic:
  extensions/copilot/src/extension/intents/node/agentIntent.ts (1386 lines)
  extensions/copilot/src/extension/intents/node/toolCallingLoop.ts (2073 lines)
  extensions/copilot/src/extension/prompts/node/agent/agentPrompt.tsx (958 lines)

Agent providers:
  extensions/copilot/src/extension/agents/vscode-node/planAgentProvider.ts (268 lines)
  extensions/copilot/src/extension/agents/vscode-node/askAgentProvider.ts (151 lines)
  extensions/copilot/src/extension/agents/vscode-node/agentTypes.ts (120 lines)
  extensions/copilot/src/extension/agents/vscode-node/promptFileContrib.ts (97 lines)

Subagents:
  extensions/copilot/src/extension/tools/node/searchSubagentTool.ts (308 lines)
  extensions/copilot/src/extension/tools/node/executionSubagentTool.ts (183 lines)
  extensions/copilot/src/extension/tools/vscode-node/switchAgentTool.ts (65 lines)

Model prompts:
  extensions/copilot/src/extension/prompts/node/agent/openai/gpt5Prompt.tsx (305 lines)
  extensions/copilot/src/extension/prompts/node/agent/openai/gpt55BasePrompt.tsx (286 lines)
  extensions/copilot/src/extension/prompts/node/agent/anthropicPrompts.tsx (706 lines)

Background agent:
  extensions/copilot/src/extension/prompts/node/agent/backgroundTodoAgent/ (4 files)

Claude integration:
  extensions/copilot/src/extension/chatSessions/claude/ (full Claude Agent SDK)
