---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 损坏的便携式Tmux修复
translated: true
type: note
---

找到了。你的便携版 `/home/lzw/bin/tmux` 自带了 `libncurses.so.6`，它编译时查找 terminfo 的路径是：

```
/opt/build/AppDir/usr/share/terminfo
```

这个路径只存在于构建机器上。而你的系统里有一个完全可用的 `/usr/bin/tmux`（来自 apt 的 v3.6a）。

**最佳修复** — 删除损坏的便携版二进制文件，使用系统自带的：

```bash
rm /home/lzw/bin/tmux
```

然后正常运行 `tmux` 即可。

---

**替代修复方案**（如果你必须保留便携版构建）：

```bash
# 选项 1：每次调用时覆盖 terminfo 路径
TERMINFO=/usr/share/terminfo /home/lzw/bin/tmux

# 选项 2：将预期路径符号链接到真实路径
sudo mkdir -p /opt/build/AppDir/usr/share
sudo ln -s /usr/share/terminfo /opt/build/AppDir/usr/share/terminfo
```

**为什么会这样：** `ww` 项目本身与此无关——有人把一个独立的 `tmux` 二进制文件（很可能是 AppImage 或便携版构建）放进了 `~/bin`，它自带的 ncurses 库有一个硬编码的 terminfo 搜索路径，来自原始构建环境。你的 shell 的 `PATH` 中 `~/bin` 很可能排在 `/usr/bin` 之前，所以损坏的那个被优先使用了。
