---
audio: false
generated: true
image: false
lang: en
layout: post
title: Layered Project Separation
translated: false
type: note
---

**Question:** What's the best way to separate projects from each other?

**Answer:**

Use layers of separation in software, from lightest to strongest. Pick the level each project actually needs.

**1. Folder and repo per project (the baseline)**

- One git repo per client or project, in its own folder.
- Never mix code across repos. Use git worktrees if you need several branches of the same project open at once.

**2. Agent context per project**

- Start a separate agent session for each project, and don't reuse one long conversation across clients.
- Keep a short notes file in each repo (for example `NOTES.md` or `CLAUDE.md`) covering goals, conventions, decisions, current status and things the agent must not touch.
- The agent reads this at the start, so you can resume any project quickly without re-explaining.

**3. Environment per project**

- Use virtual environments, version managers (like nvm, pyenv) or containers (Docker, dev containers) so dependencies don't clash between projects.
- Pin versions in lockfiles so a project builds the same way later.

**4. Credentials and accounts per project**

- Separate API keys, cloud accounts, SSH keys and repo access for each client. Never reuse one client's secrets for another.
- Use a password manager with one vault or folder per client.
- Scope permissions to the minimum the project needs.

**5. User profiles or workspaces (medium isolation)**

- Separate OS user accounts or browser profiles per client keep logins, cookies and files apart.
- This is a good middle step before buying hardware.

**6. Virtual machines or cloud dev environments (strong isolation)**

- A VM or a remote workspace (such as a cloud dev environment) gives a client a fully separate machine without buying one.
- Good when a contract requires isolation, or when a project handles sensitive data.

**7. Separate hardware (strongest, only when forced)**

- Use this only for platform or security requirements, as we discussed: iOS builds, physical device benches, or contractual rules.

**Separating your attention too**

- Cap active projects to what you can review, often 2–4.
- Work in blocks. Do one project's review and decisions together, then switch.
- Keep a simple status board (a list or kanban) showing each project's state, next step and what is waiting on a client.
- Write a quick handoff note before switching away ("where I stopped, what's next") so returning is cheap.

**Separating the business side**

- Keep separate contracts, invoices and folders for documents per client.
- Make sure each contract says who owns the code and how client data is handled.
- Never paste one client's confidential material into a session for another client.

**Rule of thumb:** start at levels 1–4 for every project, add 5 or 6 when sensitivity or conflicts call for it, and use level 7 only when a requirement leaves no choice.

**References:**

- None new. This answer is general engineering judgment rather than drawn from specific sources.
