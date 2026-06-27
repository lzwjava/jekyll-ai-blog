---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从源码构建tmux
translated: true
type: note
---

以下是完整的构建过程：

**问题：** tmux 未安装，brew 速度太慢，需要从源码构建。

**发现的依赖项：**

- tmux 需要：libevent、ncurses
- macOS 13 (Ventura) 不再在 /usr/include 中提供 ncurses 头文件
- libevent 完全未安装
- Xcode CommandLineTools 已安装（gcc、make 可用）

**步骤 1：下载源码压缩包**

```
cd ~/tmp-build
curl -fSL -o libevent-2.1.12-stable.tar.gz \
  https://github.com/libevent/libevent/releases/download/release-2.1.12-stable/libevent-2.1.12-stable.tar.gz
curl -fSL -o tmux-3.7.tar.gz \
  https://github.com/tmux/tmux/releases/download/3.7/tmux-3.7.tar.gz
```

**步骤 2：构建 libevent**（约 30 秒）

```
cd libevent-2.1.12-stable
./configure --prefix=$HOME/.local --disable-shared --disable-openssl
make -j4
make install
```

- `--disable-shared` — 仅静态库（`.a` 文件），运行时无需 `.dylib`
- `--disable-openssl` — tmux 不需要，跳过该依赖
- 安装至 `~/.local/lib/libevent*.a` 和 `~/.local/include/event2/`

**步骤 3：构建 tmux**（约 20 秒）

```
cd tmux-3.7
SDK=$(xcrun --show-sdk-path)
CFLAGS="-I$HOME/.local/include -I${SDK}/usr/include" \
LDFLAGS="-L$HOME/.local/lib" \
./configure --prefix=$HOME/.local --disable-utf8proc
make -j4
make install
```

- `CFLAGS` — 告诉 gcc 去哪里找 libevent 头文件 + macOS SDK 的 ncurses 头文件
- `LDFLAGS` — 告诉链接器去哪里找 libevent 的 `.a` 文件
- `--disable-utf8proc` — tmux 3.7 要求明确选择；我们不需要 unicode 处理支持
- SDK 路径（`xcrun --show-sdk-path`）是无需 brew 即可找到 ncurses 的关键

**步骤 4：配置 PATH**

```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

**结果：**

```
~/.local/bin/tmux 3.7
~/.local/lib/libevent*.a（静态，无运行时依赖）
```

**为何无需 brew 也能工作：**

- macOS 在 SDK 中提供了 ncurses 头文件，路径为 `/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/ncurses.h`——只需将 CFLAGS 指向该位置
- libevent 是自包含的，构建约需 30 秒
- tmux 静态链接两者，因此无需 DYLD_LIBRARY_PATH 的额外配置

**清理：** `rm -rf ~/tmp-build`——安装后不再需要源码压缩包。
