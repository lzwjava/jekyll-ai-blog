---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enhancing UX for Long LLM Waits
translated: false
type: note
---

Question: For non-streaming LLM API calls, should we show progress to the user? How should we improve the UX as context windows get longer and wait times can reach 1–5 minutes?

Answer:

You are absolutely right, and this is one of the most discussed pain points in modern LLM application design. Let me give you a comprehensive breakdown.

---

## The Core Problem

In the non-streaming case, you send a full request to the LLM API, the server generates the whole response, and when it's done, you get one response payload with the complete text. The trade-off is experience — if a response takes 5–10 seconds to generate, the user just sits there watching a spinner and has no idea whether anything is happening.

The problem isn't just that users are waiting; it's that they don't know *why* they're waiting or *how long* they'll be waiting. That uncertainty makes even short delays feel broken.

---

## Option 1: Switch to Streaming (Best Solution)

The most impactful improvement is to **stop using non-streaming calls for user-facing features** and switch to streaming.

Before using streaming, you have to wait for the final answer to be generated, often taking 3 to 15 seconds depending on answer length. With streaming, the first chunk is ready and sent to the user after just 1 second, keeping them engaged and aware of progress, even for complex queries.

Watch someone use a ChatGPT-style app for the first time and you'll notice they start reading before the response is finished. That reading-as-it-appears behavior is the whole reason streaming exists. It turns a multi-second wait into something that feels like a conversation, even when the underlying generation time hasn't budged.

Streaming implementation is simple in most SDKs:

```python
# Anthropic Python SDK
with anthropic.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "your prompt"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

---

## Option 2: If You Must Use Non-Streaming — Show Progress

When non-streaming is required (e.g., batch jobs, structured JSON output, pipelines), here are proven UX patterns:

### 1. Immediate Acknowledgment
At minimum, show the user their message immediately, disable duplicate submits, and show an in-progress state. This is basic web UX, but it's where many LLM apps fall short.

### 2. Progress Bars / Status Indicators
Add progress bars or task completion indicators, giving users real-time feedback on their request's status, making the wait feel shorter.

The psychological effect is significant: in one study, an optimized progress bar design made processes feel 11% faster than a plain version. In another, users with a moving progress bar were willing to wait about 3× longer than those with no indicator.

### 3. Async + Polling Pattern
For very long calls (1–5 min), the best architecture is:

```
User submits request
  → Backend starts async job, returns job_id immediately
  → Frontend polls /status/{job_id} every 3–5 seconds
  → Show: "Analyzing… (est. 2 min remaining)"
  → When done, fetch result
```

This lets you show real pipeline stage updates like:
- ✅ Request received
- ⏳ Processing context (128k tokens)
- ⏳ Generating response…
- ✅ Done!

### 4. Escape Hatches
If generation takes time, users tend to want escape hatches: the ability to stop generating, regenerate, continue, or ask a follow-up while the model is still finishing.

### 5. Progressive Disclosure for Long Outputs
Long answers feel slower because they're visually heavy. A short summary up front, expandable sections, "show sources" toggles, or "open in editor" for big outputs can all help reduce the perceived heaviness.

---

## Option 3: Hybrid Architecture (Best of Both Worlds)

The best production architectures combine both: stream tokens on cache misses so users see immediate progress, and serve cached responses instantly on hits so they skip the wait entirely.

For structured JSON output specifically (a common reason to avoid streaming):

- Use **streaming for the raw text** to show progress
- Use a library like `http-streaming-request` to **parse partial JSON** progressively
- Always show loading states — even with streaming, let users know something is happening. Handle errors gracefully, since network issues can interrupt streams, and implement retry logic as a fallback.

---

## Key UX Principles Summary

| Situation | Recommended Approach |
|---|---|
| Interactive chat / user watching | Always stream |
| Batch / background jobs | Non-stream + async polling + status updates |
| Long structured JSON output | Stream + partial JSON parsing |
| 1–5 min pipeline calls | Async job queue + progress stages + ETA display |
| Any non-streaming call | At minimum: instant ACK + spinner + cancel button |

---

## The Bottom Line

If a machine is waiting and nobody cares about intermediate progress, non-streaming is fine. The important part is whether you've matched the delivery mode to your actual use case and user expectations.

As context windows grow to 128k, 200k, or even 1M tokens, the pressure to **never silently block the user** becomes even more critical. The golden rule: **always communicate that work is happening**, even if you can't show exactly how much is done.

References:

- [How to Improve LLM UX: Speed, Latency & Caching](https://redis.io/blog/how-to-improve-llm-ux-speed-latency-and-caching/)
- [Zero-Wait LLMs: 8 Proven Ways to Slash GenAI Latency](https://medium.com/cyberark-engineering/zero-wait-llms-8-proven-ways-to-slash-genai-latency-a5f6cfe3d5a9)
- [Streaming LLM Responses: Make Your AI App Feel Fast](https://redis.io/blog/streaming-llm-responses/)
- [Streaming vs Non-Streaming LLMs](https://medium.com/@yrgenkuci/the-streaming-revolution-how-ais-real-time-language-models-are-changing-the-game-d9d0beb18ae2)
- [From Waiting to Streaming: Handle LLM Responses Like a Pro](https://dev.to/abhinav__ap/from-waiting-to-streaming-how-to-handle-llm-responses-like-a-pro-especially-with-json-2lgh)
