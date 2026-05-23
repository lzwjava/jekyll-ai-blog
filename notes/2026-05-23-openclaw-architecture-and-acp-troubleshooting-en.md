---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw Architecture and ACP Troubleshooting
translated: false
type: note
---

OK, I now have a thorough understanding of the OpenClaw architecture. Here's the full analysis:

---

OPENCLAW ARCHITECTURE ANALYSIS: NewsBot WeChat Issue
====================================================

HOW OPENCLAW WORKS (from the code)
-----------------------------------

OpenClaw has a fundamentally different architecture from Hermes Agent:

  ┌──────────────────────────────────────────────────────────┐
  │                    GATEWAY (server.ts)                    │
  │                  Central hub, session mgmt                │
  ├──────────────┬──────────────┬────────────────────────────┤
  │  Channels    │   Agent      │   ACP Control Plane        │
  │  (WeChat,    │   Runner     │   (external agent          │
  │   Telegram,  │   (embedded  │    processes)              │
  │   Discord,   │    PI)       │                            │
  │   ...)       │              │                            │
  └──────┬───────┴──────┬───────┴──────────┬─────────────────┘
         │              │                  │
         │         ┌────┴────┐        ┌────┴────┐
         │         │Embedded │        │ACP Agent│
         │         │PI Runner│        │Process  │
         │         │(in-proc)│        │(spawn)  │
         │         └─────────┘        └─────────┘
         │                                   │
    WeChat iLink API                   JSON-RPC/stdio
    (long-poll)                        (ACP protocol)


THE MESSAGE FLOW FOR YOUR FRIEND'S SETUP
-----------------------------------------

1. WeChat message arrives via `openclaw-weixin` channel plugin
2. Channel adapter calls `runChannelTurn()` (src/channels/turn/kernel.ts)
3. Turn kernel calls `runDispatch()` which hits the Gateway
4. Gateway resolves the agent for this session → finds "newsbot" agent
5. NewsBot agent is configured with ACP runtime
6. Gateway spawns/connects to external ACP agent process
7. Message is sent to ACP agent via ACP protocol
8. ACP agent processes message (LLM call)
9. Response comes back via ACP protocol
10. Gateway delivers response to WeChat channel
11. Channel sends reply via iLink sendmessage API

THE CRITICAL DIFFERENCE FROM HERMES
------------------------------------

In Hermes: Agent + Gateway + Channels = ONE process
In OpenClaw: Agent can be a SEPARATE process (ACP runtime)

The ACP agent process is defined in:
  - src/acp/server.ts — ACP server that connects to Gateway as a client
  - src/acp/translator.ts — translates ACP protocol ↔ Gateway calls
  - src/agents/acp-spawn.ts — spawns ACP agent processes

The ACP server connects to the Gateway via WebSocket and acts as a
client that receives prompts and sends back responses.

---

ROOT CAUSE ANALYSIS
-------------------

The diagnostic says:
  "WeChat messages are received ✅"
  "Messages are routed to NewsBot agent ✅"
  "NewsBot agent processes messages ✅"
  "Hermes integration is NOT triggered ❌"

The last line is the confusion. The "Hermes integration at /tmp/VibApp/"
is NOT part of the OpenClaw pipeline. It's a separate Node.js script
that was never connected.

The real question is: WHY is the ACP agent not sending responses back?

THREE POSSIBILITIES:

A) ACP AGENT PROCESS NOT RUNNING
   - The NewsBot ACP agent process may not be started
   - Gateway tries to connect but fails silently
   - Check: `openclaw status` or gateway logs for ACP connection errors

B) ACP AGENT PROCESS CRASHES ON PROMPT
   - The ACP agent process starts but crashes when receiving a prompt
   - The error is swallowed in the ACP protocol layer
   - Check: ACP agent process logs (stderr output)

C) AGENT CONFIG MISMATCH
   - The NewsBot agent config may point to a non-existent ACP backend
   - Or the workspace (~/.openclaw/workspace-newsbot) doesn't have
     the right config/skills/models
   - Check: `~/.openclaw/config.yaml` for the `agents.list` entry
     for "newsbot" — verify `acpBackend`, `model`, `workspace` fields

---

WHAT TO CHECK (for your friend)
-------------------------------

1. Check if ACP agent process is running:
   Look for the NewsBot ACP process in `ps aux | grep acp`

2. Check Gateway logs for ACP errors:
   Look for "acp" or "newsbot" in the gateway log output

3. Check agent config:
   Read ~/.openclaw/config.yaml — find the `agents.list` entry with
   id "newsbot". Verify:
   - `acpBackend` is set correctly
   - `model` is valid
   - `workspace` path exists

4. Check ACP session state:
   Look at `~/.openclaw/sessions/` for the NewsBot session — check
   if there are transcript files with agent responses

5. The /tmp/VibApp/ Hermes integration is IRRELEVANT
   - It's a standalone Node.js script
   - It's not connected to OpenClaw's pipeline
   - Delete it or ignore it — it's not the fix

---

BOTTOM LINE
-----------

The issue is in OpenClaw's ACP agent dispatch, not in Hermes.
The "Hermes integration" at /tmp/VibApp/ is a red herring — it was
never part of the OpenClaw pipeline.

The friend needs to:
1. Verify the NewsBot ACP agent process is actually running
2. Check gateway logs for ACP connection/prompt errors
3. Verify the agent config in ~/.openclaw/config.yaml
4. If ACP is too complex, switch NewsBot to use the embedded PI
   runtime instead (remove `acpBackend` from the agent config)

Switching to embedded PI runtime would make the flow identical to
how Hermes works — agent runs in-process, no external ACP process
to manage.