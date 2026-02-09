---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 macOS 上安装 WakeOnLan 指南
translated: true
type: note
---

Question: 如何在 macOS 上安装 wakeonlan？

Answer:

您可以使用以下主要方法之一在 macOS 上安装 `wakeonlan` 命令行工具（使用 Homebrew 是最常见且推荐的方法）。

### 推荐方法：使用 Homebrew (package manager)

1. 如果您尚未安装 Homebrew，请打开 **Terminal** 并运行：
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
   （按照屏幕上的说明操作；可能会提示输入密码。）

2. 安装 Homebrew 后，运行以下命令安装 wakeonlan：
   ```
   brew install wakeonlan
   ```

3. 安装完成后，可以直接使用：
   ```
   wakeonlan AA:BB:CC:DD:EE:FF
   ```
   （将其替换为您的目标 MAC address。如果需要，可以添加 `-i 192.168.1.255` 等选项来指定 broadcast IP。）

Homebrew 会将其安装到 `/opt/homebrew/bin/wakeonlan` (Apple Silicon) 或 `/usr/local/bin/wakeonlan` (Intel)，这些路径会自动添加到您的 PATH 中。

### 替代方案：手动安装 (无需 Homebrew)

如果您不想安装 Homebrew：

1. 打开 **Terminal** 并创建一个 bin 目录（如果还没有）：
   ```
   mkdir -p ~/bin
   ```

2. 下载 wakeonlan Perl 脚本：
   ```
   curl https://raw.githubusercontent.com/jpoliv/wakeonlan/master/wakeonlan -o ~/bin/wakeonlan
   ```

3. 赋予执行权限：
   ```
   chmod +x ~/bin/wakeonlan
   ```

4. 将 `~/bin` 添加到您的 PATH（如果尚未添加）。编辑 `~/.zshrc`（在旧版本 macOS 上为 `~/.bash_profile`）：
   ```
   echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

5. 现在可以同样使用它：
   ```
   wakeonlan AA:BB:CC:DD:EE:FF
   ```

### 其他选项

- 使用 **MacPorts** (替代 package manager)：`sudo port install wakeonlan`（不如 Homebrew 常用）。
- 存在 GUI 替代方案（例如 miniWOL 或 Wolow），但对于命令行测试，上述方法最符合 Linux `wakeonlan` 的使用习惯。

注意：在最新的 macOS 版本（如 Sequoia）上，如果在 `brew install` 后看到 Perl 相关的错误，请尝试 `brew reinstall wakeonlan` 来修复 shebang/路径。

References:

- [https://formulae.brew.sh/formula/wakeonlan](https://formulae.brew.sh/formula/wakeonlan)
- [https://www.cyberciti.biz/faq/apple-os-x-wake-on-lancommand-line-utility](https://www.cyberciti.biz/faq/apple-os-x-wake-on-lancommand-line-utility)
- [https://superuser.com/questions/411213/how-to-send-a-magic-packet-from-os-x-in-order-to-wake-a-pc-on-the-lan-wol](https://superuser.com/questions/411213/how-to-send-a-magic-packet-from-os-x-in-order-to-wake-a-pc-on-the-lan-wol)
- [https://github.com/jpoliv/wakeonlan](https://github.com/jpoliv/wakeonlan)