---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 松鼠安装修复与设置
translated: true
type: note
---

Homebrew cask 已经获取了文件（v1.1.2），但在 `sudo` 这一步失败了。我无法通过代理输入你的 macOS 密码。你需要在自己的终端中运行以下两行安装命令：

```
brew install --cask squirrel
```

它会提示你输入 macOS 密码——这对 `.pkg` 安装程序来说是正常的。

如果 brew 已经缓存了文件但拒绝重新下载，请先清除缓存：

```
brew reinstall --cask squirrel
```

安装完成后：
1. **注销并重新登录**（或重启）——macOS 需要重新登录才能识别新的输入法。
2. 前往 **系统设置 → 键盘 → 文本输入 → 编辑** → 点击 `+` → 找到“Squirrel”（鼠须管）→ 添加。
3. 按 `Ctrl+`` 或点击菜单栏中的输入法图标切换到 Squirrel。

之后我会帮你配置双拼和 rime-ice 词库。需要我在 Squirrel 安装后设置配置文件吗？