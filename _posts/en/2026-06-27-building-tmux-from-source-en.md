---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building tmux from source
translated: false
type: note
---

Here's the full build process:

**Problem:** tmux not installed, brew too slow, building from source needed.

**Dependencies discovered:**

- tmux requires: libevent, ncurses
- macOS 13 (Ventura) doesn't ship ncurses headers in /usr/include anymore
- libevent not installed at all
- Xcode CommandLineTools present (gcc, make available)

**Step 1: Download source tarballs**

```
cd ~/tmp-build
curl -fSL -o libevent-2.1.12-stable.tar.gz \
  https://github.com/libevent/libevent/releases/download/release-2.1.12-stable/libevent-2.1.12-stable.tar.gz
curl -fSL -o tmux-3.7.tar.gz \
  https://github.com/tmux/tmux/releases/download/3.7/tmux-3.7.tar.gz
```

**Step 2: Build libevent** (~30 seconds)

```
cd libevent-2.1.12-stable
./configure --prefix=$HOME/.local --disable-shared --disable-openssl
make -j4
make install
```

- `--disable-shared` — static libs only (`.a` files), no `.dylib` needed at runtime
- `--disable-openssl` — tmux doesn't need it, skip the dependency
- Installs to `~/.local/lib/libevent*.a` and `~/.local/include/event2/`

**Step 3: Build tmux** (~20 seconds)

```
cd tmux-3.7
SDK=$(xcrun --show-sdk-path)
CFLAGS="-I$HOME/.local/include -I${SDK}/usr/include" \
LDFLAGS="-L$HOME/.local/lib" \
./configure --prefix=$HOME/.local --disable-utf8proc
make -j4
make install
```

- `CFLAGS` — tells gcc where to find libevent headers + macOS SDK ncurses headers
- `LDFLAGS` — tells linker where to find libevent `.a` files
- `--disable-utf8proc` — tmux 3.7 requires explicit choice; we don't need unicode proc support
- The SDK path (`xcrun --show-sdk-path`) is the key to finding ncurses without brew

**Step 4: PATH setup**

```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

**Result:**

```
~/.local/bin/tmux 3.7
~/.local/lib/libevent*.a (static, no runtime dependency)
```

**Why this works without brew:**

- macOS ships ncurses headers inside the SDK at `/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/ncurses.h` — you just have to point CFLAGS there
- libevent is self-contained, builds in ~30s
- tmux links statically against both, so no DYLD_LIBRARY_PATH hacks needed

**Cleanup:** `rm -rf ~/tmp-build` — source tarballs no longer needed after install.
