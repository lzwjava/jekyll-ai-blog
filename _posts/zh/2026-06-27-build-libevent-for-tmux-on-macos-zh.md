---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在macOS上为tmux构建libevent
translated: true
type: note
---

Exit 127 表示命令未找到——通常是 `tmux` 的 configure 找不到 libevent，或者 `make` 未安装。但你的问题在于构建 libevent，而它是 tmux 的主要依赖项。以下是基本流程：

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

`--disable-openssl` 可避免需要 OpenSSL 头文件（tmux 不使用 libevent 的 SSL）。之后，libevent 会被安装到 `~/.local/lib` 和 `~/.local/include`，你的 tmux `CFLAGS`/`LDFLAGS` 已指向这些路径。

针对具体的 exit 127 问题——在重新构建之前，先检查实际缺失的内容：

```bash
which make gcc cc curl   # 127 通常意味着没有 make / 没有编译器
xcode-select -p          # 确保 CLT 已安装；否则执行：xcode-select --install
```

此外，你的 tmux 构建还需要 `ncurses`。macOS 自带它，但如果 configure 报错，可以用同样的方式添加，或者 `brew install ncurses` 并将 `CFLAGS`/`LDFLAGS` 指向 `$(brew --prefix ncurses)`。

在 macOS 上，如果你并非特别需要手动构建工具链，更快的做法是：

```bash
brew install tmux   # 自动拉取 libevent + ncurses
```

只有在受限制的环境中（无法使用 Homebrew）或需要自定义前缀时，从源码构建才值得。如果你的情况符合这个限制（看起来是的，因为你用了 `--prefix=$HOME/.local`），那么上面的 libevent 构建步骤就是缺失的关键部分。
