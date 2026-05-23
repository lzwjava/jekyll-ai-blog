---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Show Current Directory in Hermes
translated: false
type: note
---

Now I have the full picture. Here's the answer:

```
Question: How to know the current working directory? Is there a
command like /working-dir?

Answer:

=== NO DEDICATED /cwd COMMAND ===

There's no /cwd or /working-dir slash command in Hermes.

=== WAYS TO FIND IT ===

1. /status — does NOT show the working directory. It shows:
   - Session ID, Path (= ~/.hermes home), Model, Provider, etc.

2. Runtime footer — there IS a "cwd" field available in the
   runtime footer, but it's OFF by default. To enable it:

     /footer on

   This shows a persistent footer at the bottom of your terminal
   with model, context %, and cwd. The fields default to:
   ["model", "context_pct", "cwd"]

3. Just ask the agent — type:
     what is the current working directory?
   It will run `pwd` via the terminal tool and tell you.

4. TUI mode (--tui) — the terminal tab title includes the cwd:
     "◆ <model> · ~/projects/hermes-agent"
   So in TUI mode, the cwd IS visible in the tab title.

=== THE ACTUAL CWD VALUE ===

Hermes resolves the working directory like this:

  terminal.cwd config value (in config.yaml)
    -> if set to "." or "auto" or "cwd" -> os.getcwd()
    -> if explicit path -> that path
  TERMINAL_CWD env var overrides config
  os.getcwd() is the fallback

In practice: whatever directory you `cd`'d into before running
`hermes` is the working directory. It doesn't change during the
session.

=== RECOMMENDATION ===

If you're juggling 5-6 windows and need to know which directory
each is working in:

  /footer on     — adds a persistent footer with cwd to every prompt

Or in TUI mode it's already in the tab title.
```

So the quick answer: run `/footer on` to get cwd shown persistently. There's no `/cwd` command, but the footer field exists and is just off by default.