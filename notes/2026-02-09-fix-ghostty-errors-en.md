---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Ghostty Terminal Errors Quickly
translated: false
type: note
---

Question: Why am I getting "Error opening terminal: xterm-ghostty" when running htop and "'xterm-ghostty': unknown terminal type" with top?

Answer:

You're using **Ghostty** as your terminal emulator (likely on macOS or Linux), which sets the `TERM` environment variable to `xterm-ghostty`. This is intentional — Ghostty ships with its own terminfo entry to support its advanced features.

However, when you SSH into a remote server (or in some local environments where the terminfo database is limited), the remote system doesn't have the `xterm-ghostty` definition in its terminfo database. Programs like `htop`, `top`, `nano`, `vim`, `multitail`, and others that use **ncurses** rely on terminfo to know how to draw the UI, handle keys, colors, etc. Without it, they fail with errors like:

- `Error opening terminal: xterm-ghostty`
- `'xterm-ghostty': unknown terminal type`

This is a very common issue with newer terminal emulators (similar problems happened with kitty → `xterm-kitty`, Alacritty, WezTerm in some cases, etc.).

### Quick Fixes (choose one)

1. **Best quick fix — tell Ghostty to use a widely supported TERM value**
   Add this line to your Ghostty configuration file:

   ```
   term = xterm-256color
   ```

   - macOS location: `~/Library/Application Support/com.mitchellh.ghostty/config`
   - Linux location: `~/.config/ghostty/config`

   Save the file, **fully quit Ghostty** (not just close the window — quit the app), then restart it and open a new SSH session.
   This keeps good color support and works on almost every server without any remote changes.

2. **Override TERM only when using Ghostty (shell-based workaround)**
   Add this to your shell config on your **local** machine (e.g. `~/.zshrc` or `~/.bashrc`):

   ```bash
   if [[ "$TERM_PROGRAM" == "ghostty" ]]; then
       export TERM=xterm-256color
   fi
   ```

   Then source the file (`source ~/.zshrc`) or open a new terminal tab. This avoids changing Ghostty's config and only affects Ghostty sessions.

3. **SSH-specific fix (recommended if you only have problems over SSH)**
   Add this to your local `~/.ssh/config`:

   ```
   Host *
       SetEnv TERM=xterm-256color
   ```

   (Requires OpenSSH ≥ 8.7; very common nowadays.)
   This forces `xterm-256color` for all SSH connections without affecting local terminal usage.

4. **Proper but more work — install Ghostty's terminfo on the remote server**
   From your local machine (where Ghostty is installed):

   ```bash
   ssh user@remote-server mkdir -p ~/.terminfo/x
   scp /path/to/ghostty/terminfo/x/xterm-ghostty user@remote-server:~/.terminfo/x/
   ```

   Or follow Ghostty's official terminfo instructions: copy the compiled terminfo entry to remote machines. Some newer distros may include `xterm-ghostty` in `ncurses-term` or similar packages by 2026.

### Recommendation

Use option 1 (set `term = xterm-256color` in Ghostty config) — it's the simplest and most reliable for most people. You lose only Ghostty-specific advanced features over SSH (which usually aren't needed for `htop`/`top` anyway).

After applying the fix, both `htop` and `top` should launch normally.

References:

- [https://ghostty.org/docs/help/terminfo](https://ghostty.org/docs/help/terminfo)
- [https://travis.media/blog/ghostty-ssh-unknown-terminal-error](https://travis.media/blog/ghostty-ssh-unknown-terminal-error)
- [https://github.com/ghostty-org/ghostty/discussions/3161](https://github.com/ghostty-org/ghostty/discussions/3161)
- [https://vninja.net/2024/12/28/ghostty-workaround-for-missing-or-unsuitable-terminal-xterm-ghostty](https://vninja.net/2024/12/28/ghostty-workaround-for-missing-or-unsuitable-terminal-xterm-ghostty)
