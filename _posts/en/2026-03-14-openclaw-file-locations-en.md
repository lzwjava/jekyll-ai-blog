---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw File Locations Guide
translated: false
type: note
---

Question: When OpenClaw says it has created a todo app with `index.html`, where is the file saved on the Linux filesystem?

Answer:Question: When OpenClaw's AI agent creates a todo app with `index.html`, where is the file saved on the Linux filesystem?

Answer:

## Default Location

OpenClaw uses a dedicated workspace directory as the agent's default working directory. The default path is `~/.openclaw/workspace` — this is where all files created by the agent are saved unless you configured a different workspace path.

So your todo app is most likely at:

```
~/.openclaw/workspace/todoapp/index.html
```

or directly at:

```
~/.openclaw/workspace/index.html
```

---

## Step 1 — Find It Quickly

Run this on your server (`192.168.1.36`):

```bash
find ~/.openclaw/workspace -name "index.html"
```

Or search more broadly in case it was saved elsewhere:

```bash
find ~ -name "index.html" 2>/dev/null
```

---

## Step 2 — List Everything in the Workspace

```bash
ls -la ~/.openclaw/workspace/
```

Look for a `todoapp/` folder or `index.html` directly.

---

## Step 3 — Check if Sandbox Was Enabled

If sandboxing is enabled in your config, files are saved under `~/.openclaw/sandboxes/` instead of the main workspace.

Check if sandbox files exist:

```bash
find ~/.openclaw/sandboxes -name "index.html" 2>/dev/null
```

---

## Step 4 — Serve It in Browser (Optional)

Once you find the file, serve it with Python's built-in HTTP server:

```bash
cd ~/.openclaw/workspace/todoapp
python3 -m http.server 8080
```

Then open on your main PC:

```
http://192.168.1.36:8080
```

Don't forget UFW:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 8080
```

---

## Step 5 — Ask OpenClaw Directly

The easiest way — just ask the agent in chat:

```
where did you save the todo app? show me the full path
```

OpenClaw will tell you the exact path it wrote the file to.

---

## Summary of Possible Locations

| Scenario | Path |
| --- | --- |
| Default workspace | `~/.openclaw/workspace/todoapp/index.html` |
| Saved directly in workspace root | `~/.openclaw/workspace/index.html` |
| Sandbox enabled | `~/.openclaw/sandboxes/<id>/todoapp/index.html` |
| Older install | `~/openclaw/todoapp/index.html` |
| Custom workspace set in config | Check `agents.defaults.workspace` in `~/.openclaw/openclaw.json` |

References:

- [OpenClaw Agent Workspace - Official Docs](https://docs.openclaw.ai/concepts/agent-workspace)
- [Managing Your OpenClaw Agent Workspace](https://open-claw.bot/docs/concepts/agent-workspace/)
