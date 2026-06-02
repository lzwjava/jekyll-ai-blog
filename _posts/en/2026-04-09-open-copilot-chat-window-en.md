---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open GitHub Copilot Chat in New Window
translated: false
type: note
---

Question: How to set a key binding in VS Code so GitHub Copilot Chat moves to a separate (new) window?

Answer:

You want Copilot Chat **opened in editor / separate window**, then bind a shortcut to that command.

### Step 1 — Find the command

Open Command Palette:

```
Cmd/Ctrl + Shift + P
```

Search:

```
Chat: Open in Editor
```

This command opens Copilot Chat as a **tab**, which you can then drag to a **separate window**.

VS Code supports opening chat in different surfaces including **editor tab or separate window**. ([Visual Studio Code][1])

---

### Step 2 — Bind a key

Open keyboard shortcuts JSON:

```
Cmd/Ctrl + Shift + P
→ Preferences: Open Keyboard Shortcuts (JSON)
```

Add:

```json
{
  "key": "cmd+shift+o",
  "command": "workbench.action.chat.openInEditor"
}
```

(Windows)

```json
{
  "key": "ctrl+shift+o",
  "command": "workbench.action.chat.openInEditor"
}
```

---

### Step 3 — Move to separate window (optional)

After it opens in editor tab:

* drag the tab out
  or
* press:

```
Cmd/Ctrl + K then O
```

This opens that chat in **new VSCode window**

---

### Best setup (one-shot)

Bind directly:

```json
{
  "key": "ctrl+alt+c",
  "command": "workbench.action.chat.openInEditor"
},
{
  "key": "ctrl+alt+w",
  "command": "workbench.action.moveEditorToNewWindow"
}
```

Now:

* `Ctrl+Alt+C` → open chat in editor
* `Ctrl+Alt+W` → pop to new window

---

### Also useful Copilot Chat shortcuts

* Open chat view: `Ctrl+Alt+I`
* Inline chat: `Ctrl+I`
* Quick chat: `Ctrl+Shift+Alt+L` ([Visual Studio Code][2])

---

If you'd like, I can also set:

* toggle chat window key
* always open chat in new window
* split screen chat + code layout

[1]: https://code.visualstudio.com/docs/copilot/copilot-chat?utm_source=chatgpt.com "Chat overview"
[2]: https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features?utm_source=chatgpt.com "GitHub Copilot in VS Code cheat sheet"
