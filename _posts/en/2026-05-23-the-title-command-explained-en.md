---
audio: false
generated: true
image: false
lang: en
layout: post
title: The /title Command Explained
translated: false
type: note
---

Here's the full picture of how `/title` works:

```
Question: How does the "title" command work, when is it set or not,
and how to know the current session's title across multiple windows?

Answer:

=== THE /title COMMAND ===

`/title <name>` sets a human-readable label on the current session.
`/title` (no argument) shows the current session ID and title.

=== WHEN TITLES GET SET ===

There are TWO scenarios when you run /title:

1. Session already exists in the DB (you've sent at least one message):
   -> Title is set IMMEDIATELY via session_db.set_session_title()
   -> You see: "Session title set: <name>"

2. Session does NOT exist yet (fresh window, no messages sent):
   -> Title is QUEUED as `_pending_title`
   -> You see: "Session title queued: <name> (will be saved on first message)"
   -> On your first message, the agent loop calls _ensure_db_session(),
      which creates the DB row, then applies the pending title
   -> You see: "Session title applied: <name>"

If you resume a session (`/resume <id>`), the title shows in the
resume confirmation:  ↻ Resumed session <id> "<title>" (N messages)

=== WHAT THE TERMINAL TAB TITLE SHOWS ===

Here's the key confusion point:

- TUI mode (--tui): the terminal tab title is set to:
    "<marker> <model> · <short cwd>"
  e.g.  "◆ openrouter/anthropic/claude-sonnet-4 · ~/projects/hermes-agent"
  It does NOT show the session title. It shows the MODEL name.

- Classic CLI (no --tui): no terminal title escape sequences are
  sent at all. The terminal tab shows whatever your shell set.

So if you have 5 windows open, the terminal tabs all show the same
thing (model name + cwd), making them indistinguishable.

=== HOW TO TELL WINDOWS APART ===

1. /title (no args) — shows session ID + title for THIS window
2. /status — shows session ID, model, provider, message count
3. /sessions — lists recent sessions with their titles + IDs
4. /resume — also shows a table of sessions with titles

The session title is stored in the SQLite DB, so once set it
persists across restarts.

=== PRACTICAL TIP FOR 5-6 WINDOWS ===

The moment you open a new window and know what it's for, run:

  /title debugging-auth-bug
  /title refactor-cli-module
  /title gpu-training-experiment

Then when you're lost, /title or /sessions will tell you which
window is which. The title is queued even before your first
message, so it's safe to set immediately.

Note: the terminal TAB title (in iTerm2/Terminal.app) won't change
to match — that always shows the model name. The session title is
internal to Hermes and visible via /title and /sessions.
```

Want me to improve this? For example, I could make the TUI's terminal tab title actually show the session title instead of (or in addition to) the model name — that would directly solve your "5-6 windows" problem. Would be a small change in `ui-tui/src/app/useMainApp.ts`.
