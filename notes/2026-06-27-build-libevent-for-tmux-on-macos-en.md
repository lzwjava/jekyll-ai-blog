---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build libevent for tmux on macOS
translated: false
type: note
---

Exit 127 means a command wasn't found — likely `tmux`'s configure failing to find libevent, or `make` not installed. But your question is about building libevent, which is tmux's main dependency. Here's the minimal flow:

```bash
set -e
cd ~/tmp-build
VER=2.1.12-stable
curl -LO https://github.com/libevent/libevent/releases/download/release-${VER}/libevent-${VER}.tar.gz
tar xzf libevent-${VER}.tar.gz
cd libevent-${VER}

SDK=$(xcrun --show-sdk-path)
CFLAGS="-I${SDK}/usr/include" \
LDFLAGS="-L${SDK}/usr/lib" \
./configure --prefix=$HOME/.local --disable-openssl
make -j4
make install
```

`--disable-openssl` avoids needing OpenSSL headers (tmux doesn't use libevent's SSL). After this, libevent lands in `~/.local/lib` and `~/.local/include`, which your tmux `CFLAGS`/`LDFLAGS` already point at.

On exit 127 specifically — check what's actually missing before rebuilding:

```bash
which make gcc cc curl   # 127 often = no make / no compiler
xcode-select -p          # ensure CLT installed; else: xcode-select --install
```

Also, your tmux build needs `ncurses`. macOS ships it, but if configure complains, add it the same way or `brew install ncurses` and point `CFLAGS`/`LDFLAGS` at `$(brew --prefix ncurses)`.

A faster path on macOS, if you don't specifically need a hand-built toolchain:

```bash
brew install tmux   # pulls libevent + ncurses automatically
```

The from-source route only pays off if you're on a locked-down box without Homebrew or need a custom prefix. If that's your constraint (looks like it, given `--prefix=$HOME/.local`), the libevent block above is the missing piece.
