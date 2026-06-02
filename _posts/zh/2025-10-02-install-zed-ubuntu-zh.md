---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 在Ubuntu 24.04上安装Zed
translated: true
type: note
---

对于 Ubuntu 24.04 LTS 系统，安装 Zed（高性能代码编辑器）最直接且官方推荐的方式是通过其提供的 shell 脚本。该脚本原生支持包括基于 Debian 的 Ubuntu 在内的大多数 Linux 发行版，能自动处理依赖关系并确保获取最新稳定版本。

### 推荐安装方式：官方脚本
在终端中运行：
```
curl -f https://zed.dev/install.sh | sh
```
- 安装路径为 `~/.local/bin/zed`（如需添加到 PATH，请在 `~/.bashrc` 等配置文件中添加：`export PATH="$HOME/.local/bin:$PATH"`）
- 系统要求：您的系统（内核 6.14 上的 glibc 2.39）需满足 x86_64 架构且 glibc ≥ 2.31
- 安装完成后，可通过终端输入 `zed` 或 GNOME 应用程序菜单启动
- 预览版通道（每日构建版）：`curl -f https://zed.dev/install.sh | ZED_CHANNEL=preview sh`

若您倾向使用沙盒化通用包（无需处理原生依赖），可通过 Flatpak 选择列表中的 Flathub 选项（`dev.zed.Zed`）：
1. 安装 Flatpak（如未安装）：`sudo apt update && sudo apt install flatpak`
2. 添加 Flathub 仓库：`flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo`
3. 安装：`flatpak install flathub dev.zed.Zed`
4. 运行：`flatpak run dev.zed.Zed`

脚本安装方式通常更快速且与 GNOME 桌面环境集成度更高，而 Flatpak 更适合需要应用隔离或已习惯使用 Flatpak 的用户。请避免使用列表中其他适用于非 Debian 发行版的安装选项，这些选项在 Ubuntu 上需要额外配置才能正常运行。

### 参考文档
- [Zed Linux 安装文档](https://zed.dev/docs/linux)
- [Zed 登陆 Linux 公告](https://zed.dev/linux)
- [Repology  Zed 软件包列表](https://repology.org/project/zed-editor/versions)
