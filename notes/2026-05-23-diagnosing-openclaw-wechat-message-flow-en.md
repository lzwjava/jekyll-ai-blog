---
audio: false
generated: true
image: false
lang: en
layout: post
title: Diagnosing OpenClaw WeChat Message Flow
translated: false
type: note
---

OK, here's my analysis. I've traced the full message flow through the Hermes codebase.

---

ANALYSIS: WeChat Message Flow in Hermes Agent
==============================================

WHAT THE CODE ACTUALLY DOES (Hermes Agent)
------------------------------------------

The WeChat message pipeline in Hermes is:

1. INBOUND: WeixinAdapter._poll_loop() long-polls iLink API (getupdates)
2. PROCESS: _process_message() → builds MessageEvent → calls self.handle_message(event)
3. DISPATCH: BasePlatformAdapter.handle_message() → spawns_process_message_background()
4. AGENT: _message_handler(event) → GatewayRunner._handle_message()
5. LLM: _run_agent() → creates AIAgent → calls agent.run_conversation()
6. OUTBOUND: response goes through BasePlatformAdapter._send_with_retry()
7. SEND: WeixinAdapter.send() → iLink sendmessage API

KEY: In Hermes, the WeChat adapter and the agent are INSIDE THE SAME PROCESS.
The gateway is a monolith — platform I/O + agent loop + tool dispatch all live
in one Python process. There is no "ACP runtime" in the normal gateway flow.

The ACP adapter (acp_adapter/server.py) is a SEPARATE thing — it exposes Hermes
as an ACP server for IDE clients (VS Code, Zed, JetBrains). It does NOT connect
to the gateway's platform adapters.

---

WHAT THE FRIEND'S DIAGNOSTIC DESCRIBES
--------------------------------------

The report references:

- "NewsBot Agent" with workspace ~/.openclaw/workspace-newsbot
- "ACP (OpenClaw ACP)" runtime
- "openclaw-weixin" channel
- "Hermes integration at /tmp/VibApp/"

This is NOT a standard Hermes Agent setup. This is OpenClaw (or a fork), which
has a different architecture:

  OpenClaw architecture (inferred from the diagnostic):
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │ WeChat       │────>│ NewsBot      │────>│ ACP Runtime  │
  │ Channel      │     │ Agent        │     │ (OpenClaw)   │
  │ (openclaw-   │     │ (routing)    │     │              │
  │  weixin)     │     │              │     │              │
  └──────────────┘     └──────────────┘     └──────────────┘
                                                  │
                                                  │ NOT connected
                                                  ▼
                                          ┌──────────────┐
                                          │ /tmp/VibApp/ │
                                          │ (Hermes Node │
                                          │  integration)│
                                          └──────────────┘

---

ROOT CAUSE ANALYSIS
-------------------

The diagnostic says:

  "WeChat messages are received ✅"
  "Messages are routed to NewsBot agent ✅"
  "NewsBot agent processes messages ✅"
  "Hermes integration is NOT triggered ❌"

This makes sense. The flow is:

1. WeChat message arrives via openclaw-weixin channel
2. OpenClaw routes it to NewsBot agent
3. NewsBot dispatches to ACP runtime
4. ACP runtime processes the message (LLM call)
5. ACP runtime returns response to NewsBot
6. ??? response never reaches WeChat

The disconnect is between steps 5 and 6. There are two possible failure points:

POSSIBILITY A: ACP runtime returns response but OpenClaw doesn't relay it back

- The ACP runtime processes the message and generates a response
- But the response stays inside the ACP protocol layer
- OpenClaw's NewsBot agent doesn't forward it to the WeChat channel
- This is a bug in OpenClaw's ACP→channel bridge

POSSIBILITY B: ACP runtime fails silently

- The ACP runtime gets the message but errors out
- The error is swallowed (no logging visible to the user)
- The WeChat channel never gets a response

POSSIBILITY C: The /tmp/VibApp/ "Hermes integration" is a separate thing entirely

- It's a standalone Node.js script that was meant to be the response path
- But it's not wired into the ACP runtime at all
- It was created as a proof-of-concept but never integrated

---

WHAT TO CHECK (for your friend)
-------------------------------

1. Check ACP runtime logs — look for errors in the ACP processing step
   - In OpenClaw: look for logs related to the newsbot agent's ACP runtime
   - Check if the LLM call succeeds and returns a response

2. Check if NewsBot's response handler is wired to the WeChat channel
   - In OpenClaw config: verify that the NewsBot agent's output channel
     is set to openclaw-weixin (not just its input)

3. The /tmp/VibApp/ Hermes integration is a RED HERRING
   - It's a separate Node.js script, not part of the OpenClaw pipeline
   - The real issue is in OpenClaw's agent→channel bridge, not in Hermes

4. Test with a simpler agent first — try routing WeChat to a non-ACP agent
   in OpenClaw to see if the channel itself works

---

BOTTOM LINE
-----------

This is an OpenClaw issue, not a Hermes Agent issue. The Hermes codebase I
examined shows a clean, working WeChat pipeline (iLink long-poll → gateway
runner → AIAgent → iLink sendmessage). The friend's "NewsBot" with ACP
runtime is OpenClaw's architecture, which has a different agent dispatch
path. The /tmp/VibApp/ Hermes integration is irrelevant — it was never
connected to the OpenClaw pipeline.

The fix needs to happen in OpenClaw, specifically in how the ACP runtime's
response gets routed back to the WeChat channel adapter.
