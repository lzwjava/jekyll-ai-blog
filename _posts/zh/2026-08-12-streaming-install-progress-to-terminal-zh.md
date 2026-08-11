---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将安装进度流式传输到终端
translated: true
type: note
---

已完成。安装程序现在会将所有下载/安装进度直接显示在终端中，而非隐藏。

所做的更改：

1. **`ww/env/zed.py`**（新增）— 安装 Zed：
   - **macOS**：首先尝试 `brew install --cask zed`，失败则回退到官方脚本。
   - **Linux**：通过 `curl`（若缺少 `curl` 则使用 `wget`）运行官方安装程序，并显示**实时输出**——您能直接看到下载进度及 `sh` 执行输出，不再被抑制。
   - 检测 Zed 是否已安装（macOS 下检测 `.app`；Linux 下检测 `zed` 是否在 PATH 中）。
   - 验证脚本运行后二进制文件*确实*已出现（`curl … | sh` 管道的退出码仅反映 `sh` 的状态，可能掩盖 `curl` 的失败）。

2. **`ww/main.py`** — 接入：
   - 在 `env` 组中添加了 `zed` 路由（`from ww.env.zed import main as m`）。
   - 在顶层 `_print_help()` 和 `ww env` 使用说明中添加了帮助信息。（同时修复了之前引入的一个多余 `"` 符号。）

3. **`completions/_ww`** — 在 `env_cmds` 中添加了 `'zed:在 macOS 和 Linux 上安装 Zed 编辑器'`。

输出现在类似：
```
正在通过官方安装脚本 (curl) 安装 Zed...
  curl -fsSL https://zed.dev/install.sh | sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
  ...
```

重新加载后如需重新启用 zsh 补全：`autoload -Uz compinit && compinit`。

注意：在这台特定机器上，`curl` 和 `wget` 均未安装，安装程序会显示一条有帮助的提示（使用 `sudo apt install curl -y` 安装），而非静默失败。