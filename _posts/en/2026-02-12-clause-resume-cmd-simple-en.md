---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Claude Resume Command Explained Simply
translated: false
type: note
---

**Question:** Explain Claude's resume command

**Answer:**

The `--resume` command (or sometimes just `/resume`) is a special feature built into **Claude.ai**'s chat interface (web, desktop app, and mobile app) that lets you instantly jump back into any previous conversation by referencing its unique conversation ID.

### How it works

Typical syntax:

```
claude --resume 4cb1fd80-1234-5678-9abc-def012345678
```

or shorter versions that Claude usually accepts:

```
--resume 4cb1fd80
/resume 4cb1fd80
claude resume 4cb1fd80
```

- The number (e.g. `4cb1fd80`) is the **shortened conversation UUID**  
  Claude usually shows only the first 8 characters in the UI when you ask it “what is my current conversation id” or when it appears in share links / debug info.

### Main use cases

1. **Revive an old chat that scrolled off your history**  
   → Very long conversations sometimes disappear from the sidebar. `--resume <id>` brings it back instantly.

2. **Continue exact thread across devices / browsers**  
   → Copy the ID from one device, paste `--resume <id>` on another → same chat loads.

3. **Recover after accidentally starting new chat**  
   → Instead of copy-pasting 50 messages, just resume the old one.

4. **Share / bookmark specific conversations**  
   → People sometimes share short IDs in Discord / forums so others can load the exact same thread state (if the conversation is still accessible to their account).

### Where to find conversation IDs

- Ask Claude directly in any chat:  
  “What is the short ID of this conversation?”  
  → It usually replies with something like `Current short ID: 4cb1fd80`

- In share links:  
  `https://claude.ai/share/4cb1fd80-…` → first 8 chars are the short ID

- Sometimes visible in browser dev tools or URL parameters when you switch chats

### Limitations

- Only works **inside Claude.ai / Claude apps** (not here with Grok, not in Poe, not in third-party clients)
- Requires you to be logged into the **same Anthropic account** that created/opened the conversation
- Very old conversations (many months/years) can eventually become inaccessible even with the ID
- The short 8-char version usually works, but sometimes you need the full UUID

So in short: `--resume <id>` is Claude’s built-in “load conversation by ID” teleport command — very useful power-user feature, especially for people who generate dozens of long threads.

**References:**  

- None