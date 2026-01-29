---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Moltbot Your Private Local AI Assistant
translated: false
type: note
---

I'd be happy to give you a comprehensive introduction to clawdbot, but I need to search for current information about it first, since this appears to be a specific tool or product that I should get up-to-date details on.# Comprehensive Introduction to Clawdbot (now Moltbot)

**Clawdbot** has recently been renamed to **Moltbot** - it's an open-source personal AI assistant that runs on your own computer rather than in the cloud. Think of it as your own private AI that you control completely, accessible through messaging apps you already use.

## What Is It?

Moltbot is a personal AI assistant that runs locally on your machine and connects to messaging platforms you already use like WhatsApp, Telegram, Discord, Slack, and others. Unlike cloud-based AI services, your data stays on your device and you have full control over how it operates.

## Key Features

**Multi-Channel Access**: You can interact with Moltbot through WhatsApp, Telegram, Discord, Slack, Signal, iMessage, Microsoft Teams, Matrix, Zalo, and WebChat. It works in both direct messages and group chats.

**Persistent Memory**: The assistant remembers your conversations and preferences across sessions, building a personalized understanding of your needs over time.

**System Access**: Moltbot can read and write files, run shell commands, execute scripts, and has full system access - though you can choose to sandbox it for safety.

**Browser Control**: It can browse the web, fill forms, and extract data from websites automatically.

**Skills & Plugins**: You can extend functionality with community-created skills or build your own. The assistant can even write its own skills.

**Voice Capabilities**: On macOS, iOS, and Android, it supports voice wake commands and a talk mode for hands-free interaction.

## How It Works

Moltbot runs a Gateway control plane on your computer that connects messaging channels to an AI agent powered by models like Claude or GPT. The Gateway coordinates between:
- Your messaging apps (WhatsApp, Telegram, etc.)
- The AI model (Claude, GPT, or local models)
- System tools (browser, files, commands)
- Optional companion apps (macOS menu bar, iOS/Android)

## Installation

The easiest installation method requires Node.js 22 or higher and uses a simple npm command: `npm install -g clawdbot@latest` followed by `clawdbot onboard --install-daemon` which guides you through setup.

## Security Considerations

This is important: By default, when you use Moltbot directly (main session), it has full system access. However, for group chats or channels, you can configure it to run in sandboxed Docker containers with restricted permissions.

For messaging channels, Moltbot uses a pairing system for unknown contacts - they receive a code and you must approve them before the bot processes their messages.

## Recent Developments

**Important Security Alert**: There have been recent reports of fake VS Code extensions impersonating Clawdbot/Moltbot that install malware. Only install from official sources (the GitHub repository or npm).

The project has generated significant buzz, with over 51,000 stars on GitHub and enthusiastic community feedback. Many users describe it as feeling like "living in the future" and compare it to finally having a real Jarvis-like assistant.

## Who Created It?

Moltbot was built by Peter Steinberger and the open-source community for "Clawd," described as a space lobster AI assistant. It's an independent project with an MIT license, welcoming community contributions.

## Use Cases

People are using Moltbot for:
- Email management and unsubscribing from unwanted emails
- Calendar management and travel reminders
- Automating coding tasks and workflows
- Document processing and research
- Home automation integration
- Creating custom workflows and automations

The project represents a shift toward truly personal AI - running on your infrastructure, learning your preferences, and integrating deeply with your digital life while keeping your data private.