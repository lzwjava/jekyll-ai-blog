---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resuming Hermes Between SSH and tmux
translated: false
type: note
---

Question: Suppose we run Hermes Agent in an SSH session of a server, then cancel it and exit. Can we resume it in a tmux session, or vice versa?

Answer:

### Core Concepts

Yes, absolutely. You can seamlessly transition your Hermes Agent workspace between raw SSH sessions and `tmux` sessions. However, it is important to understand exactly **how** this works based on the framework's architecture, as there are two completely different ways to accomplish this depending on whether you want to resume the **process** or resume the **state**.

---

### Method 1: Resuming via Native Hermes Session Management (Recommended)

Hermes Agent natively abstracts session management into a persistent SQLite state database (`state.db`). Every conversation, memory context, and tool state is automatically tracked by a unique Session ID or a human-readable title.

If you abruptly kill or disconnect an SSH terminal while the agent is running:

1. The physical OS process might be terminated by the OS hangup signal (`SIGHUP`).
2. The agent's progress and conversation context are safely stored in the database.

To resume your work inside a `tmux` session (or vice versa):

* Log back into your server and attach/open your `tmux` session.
* Run the following command to pick up exactly where you left off:

```bash
hermes --continue
# OR use the shorthand flag:
hermes -c

```

> **Note:** The `--continue` or `-c` flag automatically re-attaches you to your most recent session. If you want a specific past session, you can list them with `hermes sessions list` and resume via `hermes --resume <session-id-or-title>`.
> You can also opt into automated resume behavior in the TUI by setting the environment variable `export HERMES_TUI_RESUME=1` in your shell configuration.

---

### Method 2: Resuming via Linux Process Persistence (`tmux`)

If your true goal is to prevent the agent's running terminal process from being interrupted at all when you disconnect from SSH, you should launch Hermes **inside** `tmux` from the very beginning.

* **The standard SSH pitfall:** If you start `hermes` directly in a raw SSH session and close the terminal window, the OS kills your terminal shell and everything running inside it. You can still use Method 1 (`hermes -c`) to load the state history into a new process, but any long-running tool or generation loop that was actively processing at the moment of disconnection will have been aborted.
* **The multiplexer advantage:** If you log into SSH, spin up a `tmux` multiplexer (`tmux new -s hermes_session`), and run `hermes` inside it, the process belongs to the persistent `tmux` server. If your SSH connection drops, the agent keeps executing in the background. You can reconnect via SSH later and run `tmux a -t hermes_session` to view the live terminal output precisely as you left it.
