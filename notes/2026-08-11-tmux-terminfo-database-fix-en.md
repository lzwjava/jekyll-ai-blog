---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tmux terminfo database fix
translated: false
type: note
---

Fixed. Here's what was going on and what I did:

## Root cause

Your `tmux` in `~/bin` is a custom build that links against a bundled ncurses library:

```
libncurses.so.6 => /home/lzw/bin/libs/libncurses.so.6
```

That library was compiled inside an **AppImage build environment**, so it has a hardcoded terminfo path baked in:

```
/opt/build/AppDir/usr/share/terminfo   ← doesn't exist on your machine
```

tmux looks there for the terminal definitions, fails to find them, and prints "can't find terminfo database".

The system terminfo database is fine — it's at `/usr/share/terminfo` (provided by the `ncurses-term` package).

## Fix

Set `TERMINFO=/usr/share/terminfo` so tmux uses the system database instead of the dead AppImage path. I verified it works:

```bash
TERMINFO=/usr/share/terminfo tmux
```

And made it permanent by appending to both your shell configs:

```bash
# ~/.bashrc (line 124) and ~/.zshrc (line 5)
export TERMINFO=/usr/share/terminfo
```

Open a new terminal (or run `source ~/.bashrc`) and `tmux` will work.

## Optional (cleaner alternative)

If you'd rather not keep the env var around, you could fix the library itself by symlinking the broken path to the real one — but that requires root (`/opt`). The env var is simpler and fully sufficient. If you ever recompile/update that tmux build, rebuild it against the system ncurses (`apt install libncurses-dev`) so this doesn't bite you again.
