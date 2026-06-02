---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Subagent Delegation and Failures
translated: false
type: note
---

Here's a comprehensive breakdown of how subagents work in Hermes and what happens with network issues:

## How Subagent Delegation Works

Architecture (tools/delegate_tool.py):

```
Parent Agent (your main conversation)
  └─ delegate_task tool call
       ├─ [subagent-0] ── ThreadPoolExecutor worker ── child.run_conversation()
       ├─ [subagent-1] ── ThreadPoolExecutor worker ── child.run_conversation()
       └─ [subagent-2] ── ThreadPoolExecutor worker ── child.run_conversation()
            (up to max_concurrent_children, default 3)
```

Each child gets:
- Fresh AIAgent instance (no parent conversation history)
- Own task_id (own terminal session, file ops cache)
- Restricted toolsets (delegate_task, clarify, memory, send_message, execute_code are blocked)
- Own iteration budget (default 50 iterations, configurable via delegation.max_iterations)
- Focused system prompt built from the goal + context
- Shared credential pool (children can rotate keys on rate limits)

Children run in a ThreadPoolExecutor. The parent blocks until all complete (up to child_timeout_seconds, default 600s). The parent only sees the final summary — never intermediate tool calls.

## Network Failure Handling — Two Layers

Your log shows stream drops from xiaomi. Here's exactly what's happening:

### Layer 1: Stream-level retry (inside _interruptible_streaming_api_call)

In agent/chat_completion_helpers.py, the streaming call runs in a background thread with a polling loop on the main thread. Three failure detectors:

1. Stale stream detector — if no chunks arrive within HERMES_STREAM_STALE_TIMEOUT (default 180s), kills the connection and lets the retry loop reconnect. Scales up for large contexts (>100k tokens → 300s, >50k → 240s).

2. Mid-tool-call stream drop — if the stream dies while a tool call JSON is being streamed AND the error is transient (ReadTimeout, connection reset, SSE "Network connection lost"), it silently retries up to _max_stream_retries. It resets all accumulators, rebuilds the OpenAI client connection pool, and starts fresh. The user sees "⚠ xiaomi stream drop (ReadTimeout) after 122.6s — reconnecting, retry 2/3".

3. Pre-delivery stream drop — if the stream dies before any tokens were delivered, same retry logic. After retries are exhausted, it propagates the error to the outer retry loop.

### Layer 2: Conversation-level retry (conversation_loop.py)

When the streaming layer exhausts its retries and raises, the outer loop catches the error:

- Invalid/empty responses → retry with jittered backoff (5s base, 120s cap)
- API errors (429, 500, 502, 503, 504, 524) → classified by error_classifier.py, retry with backoff
- Credential exhaustion → tries credential pool rotation, then fallback provider
- Provider fallback chain → if xiaomi keeps failing and you have fallback_model configured, it switches

The "Model returned empty after tool calls — nudging to continue" message is a different path: the model finished tool calls but returned no text content, so the loop injects a synthetic user message to nudge the model to summarize/continue.

## What Happens When the Network Changes

For subagents specifically:

1. Each child has its own API call loop. A network change mid-task means every in-flight HTTP request hits ReadTimeout or connection reset.

2. The stream-level retry will fire for each subagent independently (that's why you see [subagent-0], [subagent-1], [subagent-2] all dropping simultaneously around 122-123s).

3. If the network recovers within the retry window (typically 3 attempts), the subagents silently reconnect and continue. Their conversation history is preserved — the retry replays the same API call with the same messages.

4. If the network stays down through all retries:
   - Stream layer raises the error
   - Conversation layer retries with backoff
   - If still failing, tries fallback provider (if configured)
   - If all exhausted, the child returns {"failed": True, "error": "..."}
   - Parent sees a "failed" entry in the delegation results and reports it

5. The child_timeout (default 600s) is the hard cap. A subagent stuck on network issues will eventually timeout. The heartbeat thread (30s interval) monitors child progress — if neither iteration count nor current_tool advances for 15 cycles (450s idle), it stops touching the parent's activity, letting the gateway timeout fire.

6. Each subagent rebuilds its OpenAI client on retry (agent._replace_primary_openai_client), purging dead connections from the pool.

## Key config knobs

- delegation.child_timeout_seconds — hard per-child timeout (default 600)
- delegation.max_iterations — per-child iteration cap (default 50)
- delegation.max_concurrent_children — parallel children (default 3)
- HERMES_STREAM_STALE_TIMEOUT — override stale stream detection (env var)
- Fallback model chain — in config.yaml, so children inherit the parent's fallback chain

The short answer: network changes during subagent execution cause parallel stream drops across all children. Each child retries independently at both the stream level (3 attempts, connection rebuild) and the conversation level (backoff + credential rotation + fallback). If the network recovers within ~5-10 minutes, most subagents will transparently resume. If not, they fail gracefully and the parent gets error summaries instead of results.
