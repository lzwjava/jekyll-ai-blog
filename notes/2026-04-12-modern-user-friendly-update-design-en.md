---
audio: false
generated: true
image: false
lang: en
layout: post
title: Modern and User-Friendly Software Update Design
translated: false
type: note
---

Question: Is the hermes update command cool? Is it a fancy way to handle updates? What do I think about it?

Answer:

Yes, the `hermes update` command is indeed quite cool and demonstrates a thoughtful, user-friendly approach to managing software updates.

Here's why I think it's fancy and well-designed:

- **Smart local change handling**: It automatically detects local modifications, stashes them before pulling updates, and then offers to restore them afterward. This prevents accidental loss of customizations while still allowing a clean update. The clear warnings about reviewing `git diff` or `git status` afterward show good attention to potential conflicts.

- **Upstream remote management**: It notices when you're on a fork and proactively suggests (and adds) the official upstream repository. This helps users stay in sync with the main project without missing important updates from NousResearch.

- **Dependency updates**: It automatically handles both Python and Node.js dependency updates, which is convenient for a project that likely mixes backend and browser-related tools.

- **Cleanup and maintenance**: Clearing stale `__pycache__` directories and syncing bundled skills (adding new ones, updating others, removing outdated ones) keeps the environment clean and current.

- **Configuration awareness**: It checks for new configuration options, ensuring your setup stays compatible without manual intervention.

- **Helpful post-update tips**: Suggesting how to select a provider and model right after the update guides users toward next steps.

Overall, this update process feels modern, safe, and polished. It treats the user as someone who might have made custom changes (common in agent/AI tool projects) and handles the complexity behind the scenes while keeping everything transparent. Many CLI tools just do a blind `git pull` and leave users to deal with messes — Hermes does the opposite by being proactive and communicative.

It's a great example of developer experience (DX) done right in an open-source AI agent project. The interactive prompts (Y/n choices) make it feel guided rather than scary for less git-savvy users.

If you're using Hermes Agent regularly, this kind of smooth update flow definitely makes maintenance less of a chore and more enjoyable.

References:
- https://github.com/NousResearch/Hermes-Agent.git
