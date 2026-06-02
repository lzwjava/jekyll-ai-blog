---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes-Agent Note Workflow Redirection
translated: false
type: note
---

We modified the `ww note` command to redirect users to the hermes-agent `/note` plugin:

1. First attempt: blocked `ww note` entirely, requiring `--manual` flag to run. This failed because `_pop_subcmd()` consumed `--manual` as a subcommand name.

2. Second attempt: replaced the block with an interactive prompt — "Continue with standalone note workflow? [Y/n]". Worked but you wanted simpler UX.

3. Final version: prompt changed to "Press Enter to continue, Ctrl+C to quit..." — no Y/n parsing, just Enter to proceed or Ctrl+C to bail.

The net effect: running `ww note` now shows a tip pointing to `/note` in hermes-agent, then waits for Enter confirmation before running the original standalone workflow. Subcommands like `ww note log` and `ww note obfuscate` are unaffected.
