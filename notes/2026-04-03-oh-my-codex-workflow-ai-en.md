---
audio: false
generated: true
image: false
lang: en
layout: post
title: Introduction to Oh My Codex Workflow AI
translated: false
type: note
---

I'll search for information about oh-my-codex to provide you with a comprehensive introduction.Question: What is a comprehensive introduction to oh-my-codex, a workflow AI built on top of Codex?

Answer:

## Overview

Oh My Codex (OMX) is a multi-agent orchestration layer designed to extend the capabilities of OpenAI Codex CLI by introducing structured teamwork, automation, and advanced workflow management. It coordinates up to 30 role-specialized agents and 40+ workflow skills to automate coding lifecycles. Think of it as an enhancement layer that transforms Codex from a single AI coding assistant into a coordinated system of specialized agents working in parallel.

## Core Purpose

OMX addresses limitations in the base Codex environment, such as the lack of hooks, agent coordination, and persistent execution, by layering a shell-based system that enables richer interaction patterns. It keeps Codex as the execution engine and makes it easier to run structured workflows, allowing developers to delegate complex, multi-step tasks to AI teams rather than managing everything manually.

## Key Components

### 1. Multi-Agent System

OMX provides 33 specialized role-based prompts organized into tiers:

- **Core Development**: architect, planner, executor, debugger, verifier
- **Quality Assurance**: style-reviewer, quality-reviewer, api-reviewer, security-reviewer, performance-reviewer
- **Domain Experts**: dependency-expert, test-engineer, build-fixer, designer, writer
- **Product Strategy**: product-manager, ux-researcher, product-analyst

These agents can be invoked using the `/prompts:name` syntax for targeted expertise.

### 2. Workflow Skills

OMX includes 36 workflow skills accessible via dollar-sign syntax for autopilot, team orchestration, planning, recovery, and QA cycles. Key workflows include:

- **`$autopilot`**: Full autonomous execution from idea to working code
- **`$ralph`**: Self-referential completion loop with verification until done
- **`$team`**: Coordinated parallel execution with N workers
- **`$plan`**: Strategic planning with consensus review modes
- **`$tdd`**: Test-driven development with red-green-refactor cycle
- **`$research`**: Parallel research agents for comprehensive investigation
- **`$security-review`**: Security audits focusing on vulnerabilities

### 3. Team Mode with Automatic Worktrees

Since version 0.10.0, every team worker runs in an isolated git worktree by default, enabling conflict-free parallel development without manual branch management. This means:

- Each worker gets a dedicated worktree at `.omx/team/<n>/worktrees/worker-N`
- Workers write to isolated detached branches while the leader workspace stays clean
- The leader continuously integrates worker commits via merge, cherry-pick, or cross-worker rebase strategies, with conflicts detected early and reported
- Auto-commit ensures no work is lost

The system leverages tools like tmux to manage multiple agent sessions simultaneously, enabling a team mode where different agents handle distinct responsibilities within a shared workflow.

### 4. Persistent State and Memory

OMX provides five MCP (Model Context Protocol) servers for persistent context and cross-session learning:

- State server
- Memory server
- Code intelligence server
- Trace server
- Session-specific notepads

This allows workflows to maintain context across sessions and learn from previous interactions.

### 5. Staged Pipeline Execution

Tasks move through structured phases: plan → prd (product requirements document) → exec (execute) → verify → fix lifecycle for evidence-based development workflows. This ensures systematic progression through development stages with built-in quality gates.

## Workflow Patterns

### Standard Workflow Path

The main workflow follows: deep-interview to clarify requirements, ralplan to approve the implementation plan and review tradeoffs, ralph to carry the approved plan to completion, or team for coordinated parallel execution.

### Launch Modes

OMX offers granular control over reasoning effort through launch profiles:
- `--yolo`: Quick execution with minimal validation
- `--high`: Increased reasoning effort
- `--xhigh`: Maximum reasoning depth
- `--madmax`: Extreme mode for complex challenges

### Mixed Provider Support

OMX supports running Codex, Claude, and Gemini workers side-by-side using the OMX_TEAM_WORKER_CLI_MAP configuration. This allows teams to leverage different AI providers based on their strengths.

## Recent Features (v0.10.0)

The latest version introduced several major enhancements:

1. **Autonomous Research**: `omx autoresearch` launches iterative research loops that explore topics, refine questions, and synthesize findings
2. **Orchestration Wrapper**: `omx exec` runs any command through the OMX layer with hooks, state tracking, and logging
3. **Intent-First Deep Interviews**: Intent classification happens upfront before Socratic questioning, routing to workflows faster
4. **Incremental Merge Tracking**: Smarter conflict detection tracks worktree changes incrementally

## Integration Capabilities

OMX integrates with external services through:

- **Discord**: Real-time notifications, webhook integration, and bot commands
- **Telegram**: Mobile notifications and command interface
- **OpenClaw Gateway**: Unified delivery for Discord, Slack, Telegram, and custom webhooks
- **MCP Servers**: For persistent state and external service integration

## Installation and Usage

```bash
# Install globally
npm install -g oh-my-codex

# Setup and verify
omx setup && omx doctor

# Example usage
omx autoresearch "how does the auth middleware work?"
omx team 3:executor "refactor auth module with full test coverage"
```

## Use Cases

OMX is ideal for complex project automation, large-scale code generation, coordinated code review and security audits, test-driven development pipelines, and reproducible multi-agent CI/automation environments.

## Philosophy

OMX does not replace Codex - it's better task routing plus better workflow plus better runtime, not a command surface to operate manually all day. It's designed for developers who already use Codex and want enhanced orchestration, persistent state, and multi-agent coordination capabilities layered on top.

References:

- [https://github.com/Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
- [https://sourceforge.net/projects/oh-my-codex-omx.mirror/](https://sourceforge.net/projects/oh-my-codex-omx.mirror/)
- [https://github.com/staticpayload/oh-my-codex](https://github.com/staticpayload/oh-my-codex)
- [https://mcpmarket.com/server/oh-my-codex](https://mcpmarket.com/server/oh-my-codex)
- [https://yeachan-heo.github.io/oh-my-codex-website/](https://yeachan-heo.github.io/oh-my-codex-website/)
- [https://lobehub.com/skills/neversight-learn-skills.dev-oh-my-codex](https://lobehub.com/skills/neversight-learn-skills.dev-oh-my-codex)
- [https://yeachan-heo.github.io/oh-my-codex-website/docs.html](https://yeachan-heo.github.io/oh-my-codex-website/docs.html)