---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dangerous Flag Ignores Directory Limits
translated: false
type: note
---

Question:
In Claude Code, when using `--dangerously-skip-permissions`, does it only take effect in the current directory, and will it avoid deleting files outside the current directory?

Answer:

No. The flag `--dangerously-skip-permissions` **is not restricted to the current directory**. It **does not sandbox Claude to the current working directory**, and it **can potentially modify or delete files outside the current directory** depending on what commands or tools it runs.

### 1. What the flag actually does

When you start Claude Code with:

```
claude --dangerously-skip-permissions
```

you enable **bypass permissions mode** (sometimes called *YOLO mode*). In this mode:

* All tool operations are **automatically approved**
* No confirmation prompts appear
* Claude can run:

  * file read/write operations
  * shell commands
  * network requests
  * git commands
  * system operations

Everything is executed **without user confirmation**. ([AGCMD][1])

### 2. Scope is the full environment, not just the current directory

The CLI itself does **not enforce a directory boundary**. If Claude decides to run a shell command like:

```
rm -rf ../some_folder
```

or

```
rm -rf ~
```

those commands will run normally if the OS allows them.

So the effective scope is:

* **Whatever the current user account has permission to access**
* Not just the project folder

That means it could theoretically affect:

* parent directories
* your home directory
* system files (if running with elevated privileges)

### 3. Why the flag is called “dangerously”

The flag name is intentionally explicit because it removes all safety checks. This means a single incorrect instruction or hallucinated command could cause destructive operations such as deleting files or modifying system state. ([ClaudeLog][2])

Examples of possible consequences:

* accidental `rm -rf` commands
* destructive git operations
* modifying configuration files
* overwriting unrelated directories

### 4. How developers usually make it safe

Experienced users typically run it in **isolated environments**, such as:

1. **Inside a container**

   * Docker devcontainer
   * ephemeral CI runner

2. **Inside a project workspace**

   * only mount the repo folder

3. **Using git protection**

   * revert changes if needed

Example safe workflow:

```
docker run -it -v ./project:/workspace dev-env
cd /workspace
claude --dangerously-skip-permissions
```

Then the worst damage is limited to `/workspace`.

### 5. Practical rule of thumb

Think of this flag as:

> “Claude can run any command that you could run in the terminal.”

So it is **not directory-scoped**, and it **can modify files outside the current folder**.

If you want safer behavior, use:

* `allowedTools` configuration
* permission prompts
* containerized environments

---

If you want, I can also explain **how Codex, Claude Code, and Cursor sandbox file access differently**, because their security models are actually quite different.

[1]: https://agcmd.com/?utm_source=chatgpt.com "claude --dangerously-skip-permissions | Skip Permissions Claude Code CLI"
[2]: https://claudelog.com/faqs/what-is-dangerously-skip-permissions/?utm_source=chatgpt.com "What is Dangerously Skip Permissions in Claude Code | ClaudeLog"