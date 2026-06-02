---
audio: false
generated: true
lang: zh
layout: post
title: 在Ubuntu系统中卸载Outline VPN客户端
translated: true
type: note
---

看起来 `apt` 找不到名为 `outline-client` 的软件包。这通常意味着两种情况之一：

1. **您没有使用 `apt` 安装 Outline（即它不是作为 .deb 包安装的）。** 这是 Outline 出现此错误的最常见原因，因为许多用户是通过 AppImage 安装的。
2. **软件包名称不同，或者软件源未配置。** 虽然对于 Outline 来说可能性较小，但对于其他软件来说是一种可能。

鉴于您之前的尝试，您很可能将其安装为 **AppImage**。在这种情况下，您需要手动删除它。

以下是操作步骤：

**1. 找到并删除 AppImage 文件：**

当 Outline 客户端作为 AppImage 安装时，通常是一个单独的可执行文件。您可能将其下载到了 `Downloads` 文件夹，或者可能将其移动到了您主目录中的 `bin` 或 `Applications` 文件夹。

* **需要检查的常见位置：**
  * `~/Downloads/`
  * `~/Applications/`（如果您创建了此文件夹）
  * `~/bin/`（如果您创建了此文件夹）
  * 您最初运行它的目录。

* **如何找到它：** 您可以使用 `find` 命令在您的主目录中搜索它：

    ```bash
    find ~ -name "Outline-Client*.AppImage" 2>/dev/null
    ```

    此命令将在您的主目录中搜索任何以 "Outline-Client" 开头并以 ".AppImage" 结尾的文件。
    找到后，将其删除：

    ```bash
    rm /path/to/Outline-Client.AppImage
    ```

    （将 `/path/to/` 替换为 `find` 命令找到的实际路径。）

**2. 删除残留的配置和自启动文件：**

即使您删除了 AppImage，Outline 可能也创建了一些配置文件和自启动项。

* **删除配置目录：**

    ```bash
    rm -rf ~/.config/Outline/
    ```

    此命令会删除您用户配置文件夹中的整个 `Outline` 目录。

* **删除自启动项（如果已创建）：**
    如果 Outline 被设置为在您登录时自动启动，可能会有一个对应的 `.desktop` 文件。

    ```bash
    rm -f ~/.config/autostart/Outline-Client.AppImage.desktop
    ```

* **删除桌面图标（如果有）：**
    有时 AppImage 会在您的本地图标目录中创建桌面图标。

    ```bash
    find ~/.local/share/icons -name "appimagekit-outline-client*.png" -delete
    ```

    这将删除与 Outline AppImage 相关的任何 PNG 图标。

**3. 检查并恢复网络配置（如有必要）：**

与其他 VPN 一样，Outline 可能会修改您的 DNS 设置。如果在删除 AppImage 后遇到互联网连接问题，请检查您的 `/etc/resolv.conf` 文件。

* **检查 `resolv.conf`：**

    ```bash
    cat /etc/resolv.conf
    ```

    查找看起来像是被 Outline 添加的行（例如，您不认识作为路由器或 ISP DNS 的特定名称服务器 IP 地址）。

* **恢复 `resolv.conf`（如果需要）：**
    如果它看起来被 Outline 修改过：
  * **选项 A（适用于现代 Ubuntu 的推荐方法）：** 如果您的系统使用 `systemd-resolved`（这在最近的 Ubuntu 版本中很常见），通常可以通过重新创建符号链接来修复：

        ```bash
        sudo rm /etc/resolv.conf
        sudo ln -s /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
        ```

  * **选项 B（手动编辑 - 如果选项 A 无效或用于旧系统）：**
        首先，进行备份：

        ```bash
        sudo cp /etc/resolv.conf /etc/resolv.conf.bak
        ```

        然后，编辑该文件：

        ```bash
        sudo nano /etc/resolv.conf
        ```

        注释掉或删除任何由 Outline 添加的 `nameserver` 行。如果您不确定 ISP 的 DNS，通常可以填入公共 DNS 服务器，例如 Google 的（`8.8.8.8` 和 `8.8.4.4`）或 Cloudflare 的（`1.1.1.1` 和 `1.0.0.1`）。

**4. 重启系统：**

完成这些步骤后，强烈建议您重新启动 Ubuntu 系统，以确保所有更改生效，并且与 Outline 相关的任何后台进程被完全终止。

```bash
sudo reboot
```

通过遵循这些手动删除步骤，您应该能够从 Ubuntu 系统中完全移除 Outline VPN 客户端。
