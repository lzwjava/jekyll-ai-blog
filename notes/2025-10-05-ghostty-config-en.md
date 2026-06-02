---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Ghostty Shell Configuration Guide
translated: false
type: note
---

### Ghostty and .bashrc on Ubuntu

Ghostty behaves similarly to the default GNOME Terminal on Ubuntu (and other Linux distros) when it comes to loading `.bashrc`. By default, Ghostty starts **non-login interactive shells** for bash, which means it sources `~/.bashrc` directly—just like GNOME Terminal. This is the standard behavior for most Linux terminals, where `.bashrc` handles interactive shell setup (e.g., aliases, prompts, environment variables for non-login sessions).

#### How It Loads .bashrc

- When you open a new Ghostty window or tab, it executes `bash` (or your default shell) as a non-login shell.
- Bash checks for and sources `~/.bashrc` if the shell is interactive (which it is by default).
- If you have a `~/.bash_profile` (typically for login shells), it won't be sourced unless you explicitly configure Ghostty to start a login shell (e.g., by adding `initial-command = bash --login` to `~/.config/ghostty/config`).
- Potential issues: Some users report `.bashrc` not loading on first launch for new users or in specific setups (e.g., remote SSH sessions on Ubuntu). This can often be fixed by ensuring no conflicting `~/.bash_profile` exists, or by manually sourcing it in your config. Adding a guard in `.bashrc` like `[[ $- != *i* ]] && return` can prevent issues in non-interactive contexts.

In short, yes—Ghostty is the same as the default Terminal for using `.bashrc` on Ubuntu, with the same non-login default.

### Ghostty on macOS: .zprofile or .bash_profile?

On macOS, Ghostty follows the platform's tradition (like Terminal.app) and starts **login shells** by default, regardless of the shell. This affects which profile loads:

- **If using zsh (macOS default since Catalina)**: It sources `~/.zprofile` (for login setup) *and* `~/.zshrc` (for interactive setup) every time a new terminal opens.
- **If using bash**: It sources `~/.bash_profile` (login shell). Bash won't source `~/.bashrc` directly here—`~/.bashrc` is only for non-login interactive shells. To include `.bashrc` content, add this to your `~/.bash_profile`:

  ```
  if [ -f ~/.bashrc ]; then . ~/.bashrc; fi
  ```

So, it loads `~/.zprofile` for the default zsh setup, or `~/.bash_profile` if you're using bash. You can switch shells or tweak via Ghostty's config if needed.

[Shell Integration - Ghostty](https://ghostty.org/docs/features/shell-integration)
[macOS Login Shells - Ghostty](https://ghostty.org/docs/help/macos-login-shells)
[Potential bug, .bashrc not read on startup - GitHub Discussion](https://github.com/ghostty-org/ghostty/discussions/3437)
[Bash Startup Files - GNU Manual](https://www.gnu.org/software/bash/manual/bash.html#Bash-Startup-Files)
