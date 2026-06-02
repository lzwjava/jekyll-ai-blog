---
audio: false
generated: true
image: false
lang: en
layout: post
title: Copilot Chat Window Workflow Setup
translated: false
type: note
---

Question: Are “Chat: Move Chat into New Window (Cmd+L)” and “Chat: New Chat Editor” useful key bindings, and how should they be used?

Answer:

Yes — these two commands together give the cleanest **separate Copilot Chat window workflow**.

### 1. Chat: Move Chat into New Window

This moves the **current Copilot chat** into its own VS Code window.

Recommended binding:

```json
{
  "key": "cmd+l",
  "command": "workbench.action.chat.moveToNewWindow"
}
```

What it does:

* keeps current conversation
* detaches chat into standalone window
* best for multi-monitor workflow

---

### 2. Chat: New Chat Editor

This creates a **new chat tab** (like opening a new document)

Recommended binding:

```json
{
  "key": "cmd+shift+l",
  "command": "workbench.action.chat.openInEditor"
}
```

What it does:

* new independent chat
* lives in editor tab
* can then move to new window

---

### Best workflow

1. `Cmd + Shift + L` → new chat editor
2. `Cmd + L` → move to new window

Result:

* one window = code
* one window = Copilot
* multiple chats possible

This is currently the **cleanest Copilot power-user setup**.
