---
audio: false
generated: true
image: false
lang: en
layout: post
title: Broken Portable Tmux Fix
translated: false
type: note
---

Found it. Your portable `/home/lzw/bin/tmux` bundles its own `libncurses.so.6`, which was compiled to look for terminfo at:

```
/opt/build/AppDir/usr/share/terminfo
```

That path only existed on the build machine. Meanwhile, your system has a perfectly good `/usr/bin/tmux` (v3.6a from apt).

**Best fix** — remove the broken portable binary and use the system one:

```bash
rm /home/lzw/bin/tmux
```

Then just run `tmux` normally.

---

**Alternative fixes** (if you must keep the portable build):

```bash
# Option 1: Override terminfo path per invocation
TERMINFO=/usr/share/terminfo /home/lzw/bin/tmux

# Option 2: Symlink the expected path to the real one
sudo mkdir -p /opt/build/AppDir/usr/share
sudo ln -s /usr/share/terminfo /opt/build/AppDir/usr/share/terminfo
```

**Why this happened:** The `ww` project itself is unrelated — someone dropped a standalone `tmux` binary (likely an AppImage or portable build) into `~/bin`, and its bundled ncurses library has a hardcoded terminfo search path from the original build environment. Your shell's `PATH` likely has `~/bin` before `/usr/bin`, so the broken one wins.
