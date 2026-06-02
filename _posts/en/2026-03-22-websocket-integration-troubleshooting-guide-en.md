---
audio: false
generated: true
image: false
lang: en
layout: post
title: WebSocket Integration and Troubleshooting Guide
translated: false
type: note
---

These are separate concerns:

**Why WebSocket?**

OpenClaw uses WebSocket as its core real-time transport between the browser Control UI and the gateway process. The gateway runs as a persistent background service that manages AI agents, message routing, and channel connections. WebSocket gives:
- Bidirectional, low-latency streaming (AI responses stream token-by-token to the UI)
- Persistent connection so the gateway can push events (new messages, agent status) to the browser without polling
- A single connection that multiplexes many concurrent sessions/agents

The URL `ws://192.168.1.36:18789` is just the plain-HTTP equivalent of the gateway's WebSocket endpoint — same host/port as the HTTP server, but upgraded to WebSocket protocol.

**Copy button issue**

Likely related, yes. The copy button in the Control UI almost certainly uses the WebSocket connection to send a command to the gateway (e.g. copy message content via the native clipboard on the gateway host). If the WS connection isn't fully established or is being dropped, any button that fires a WS message will silently fail or error.

Fix the WS connection first (origin allowlist + `dangerouslyDisableDeviceAuth`), then retest the copy button.
