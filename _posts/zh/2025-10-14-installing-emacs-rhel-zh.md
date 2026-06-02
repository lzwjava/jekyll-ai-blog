---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在RHEL系统上安装Emacs
translated: true
type: note
---

### 在 Red Hat Enterprise Linux 上安装 Emacs

Red Hat Enterprise Linux (RHEL) 主要使用 DNF 包管理器来安装软件。Emacs 在默认软件仓库中即可获取，因此安装过程十分简单。以下步骤适用于现代版本（RHEL 8 及更高版本）。对于旧版本（如 RHEL 7），请将 `dnf` 替换为 `yum`。

#### 前置条件

- 确保您拥有 root 权限（使用 `sudo`）。
- 如果使用官方 RHEL 软件仓库，您的系统应已注册 Red Hat Subscription Management。

#### 安装步骤

1. **更新软件包缓存**（推荐操作以确保获取最新可用版本）：

   ```
   sudo dnf update
   ```

2. **安装 Emacs**：

   ```
   sudo dnf install emacs
   ```

   这将安装软件仓库中可用的最新稳定版本（例如，根据您的 RHEL 版本，可能是 Emacs 28.x 或 29.x）。

3. **验证安装**：
   运行以下命令检查版本：

   ```
   emacs --version
   ```

   您应该看到类似 `GNU Emacs 28.2` 的输出（或类似信息）。

#### 注意事项

- 如果您使用的是旧版 RHEL（如 RHEL 7），请使用命令 `sudo yum install emacs`。
- 要获取最新版本（例如 29+），您可能需要从源码编译或使用第三方软件仓库（如 EPEL），因为基础软件仓库的版本可能较旧。
- 要启动 Emacs，只需在终端中输入 `emacs`。

[GNU Emacs 常见问题：安装 Emacs](https://www.gnu.org/software/emacs/manual/html_node/efaq/Installing-Emacs.html)
[Red Hat 文档：使用 DNF 管理软件](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html-single/managing_software_with_the_dnf_tool/index)
