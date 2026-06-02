---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 解决Ghostty的GLIBC版本冲突问题
translated: true
type: note
---

你遇到的问题不仅仅是安装冲突——主要是 Snap 和你下载的 `.deb` 包都是基于 GLIBC 2.38（来自 Ubuntu 24.04）构建的，但你的系统是 Ubuntu 22.04（根据你 `libc-bin` 包中的 GLIBC 2.35 版本判断）。这导致在尝试运行二进制文件时出现“未找到版本 `GLIBC_2.38'”的错误。同时启用两个安装版本也可能导致路径冲突（例如，具体执行哪个`ghostty` 二进制文件），所以是的，你应该先卸载它们以清理环境。

### 步骤 1：移除现有安装

运行以下命令卸载两者：

```
sudo snap remove ghostty
sudo apt remove ghostty
```

- 这将移除 Snap 版本和 `.deb` 版本，不会影响系统的其他部分。
- 使用 `which ghostty`（应不返回任何内容）和 `snap list | grep ghostty`（应为空）验证卸载。

### 步骤 2：安装兼容版本

Ghostty 目前没有为 Ubuntu 22.04 提供官方的 `.deb` 包，但有一个可靠的非官方仓库为其（及其他版本）构建兼容的 `.deb` 文件。它会自动处理 GLIBC 兼容性问题。

最简单的方法是使用他们的自动安装脚本，该脚本会检测你的 Ubuntu 版本并获取正确的包：

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/mkasberg/ghostty-ubuntu/HEAD/install.sh)"
```

- 这会下载并安装最新的兼容 `.deb` 包（截至近期发布，目前大约为 v1.2.x）。
- 完成后，运行 `ghostty` 进行测试——它应该能正常启动，不会出现 GLIBC 错误。
- 如果在安装过程中出现任何依赖项提示（例如对于 `libonig5`），只需用 `Y` 批准即可。

如果你偏好手动安装：

1. 前往[发布页面](https://github.com/mkasberg/ghostty-ubuntu/releases)。
2. 下载标有 Ubuntu 22.04 的 `.deb` 文件（例如，名称可能类似 `ghostty_1.2.1-0.ppa1_amd64_22.04.deb`——具体名称因发布版本而异）。
3. 使用 `sudo dpkg -i ghostty_*.deb` 进行安装（在下载文件夹中运行）。
4. 如果它抱怨缺少依赖项，请使用 `sudo apt install -f` 进行修复。

### 补充说明

- **为什么这里不需要从源码构建**：非官方仓库已经为你完成了繁重的工作，但如果你想自己构建 Ghostty（例如，为了自定义版本），请遵循[官方源码构建指南](https://ghostty.org/docs/install/build)。它需要 Zig 0.13 和一些依赖项如 `libgtk-4-dev`，但使用 `.deb` 方式更简单。
- **考虑升级 Ubuntu？** 如果你愿意，升级到 24.04 可以让你使用官方 Snap 或你之前尝试的 24.04 `.deb` 包而不会出现问题。
- 安装后，你可以通过 `~/.config/ghostty/config` 配置 Ghostty（有关选项，请参阅[文档](https://ghostty.org/docs/config)）。

如果在这些步骤中遇到任何错误，请将输出粘贴到这里以获取更多帮助！
