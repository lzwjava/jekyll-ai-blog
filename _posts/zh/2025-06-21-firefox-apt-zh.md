---
audio: false
generated: true
lang: zh
layout: post
title: 在 Ubuntu 上通过 APT 安装 Firefox
translated: true
type: note
---

本指南详细介绍如何在 Ubuntu 系统中通过 Mozilla APT 仓库安装 Firefox，以替代默认的 Snap 软件包。

**为何选择 APT 版本？**

虽然 Snap 版本安装便捷，但部分用户更青睐 APT 版本，因其具有更好的系统集成性与性能表现。

**操作步骤：**

1. **卸载 Firefox Snap 版本：**

    ```bash
    sudo snap remove firefox
    ```

2. **创建 APT 密钥环目录（如尚未存在）：**

    ```bash
    sudo install -d -m 0755 /etc/apt/keyrings
    ```

3. **导入 Mozilla APT 仓库签名密钥：**

    ```bash
    wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | sudo tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
    ```

    *若系统中未安装 `wget`，请先执行：`sudo apt install wget`*

4. **将 Mozilla 仓库添加至软件源列表：**

    ```bash
    echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | sudo tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
    ```

5. **设置软件包优先级以优先选用 Mozilla DEB 版本：**

    此操作可防止 Ubuntu 的过渡软件包重新安装 Snap 版本。

    ```bash
    echo '
    Package: *
    Pin: origin packages.mozilla.org
    Pin-Priority: 1000

    Package: firefox*
    Pin: release o=Ubuntu
    Pin-Priority: -1' | sudo tee /etc/apt/preferences.d/mozilla
    ```

6. **移除 Ubuntu Firefox DEB 版本（如存在）并安装 Mozilla 版本：**

    ```bash
    sudo apt update && sudo apt remove firefox
    sudo apt install firefox
    ```

现在您已通过官方 Mozilla APT 仓库成功安装 Firefox！
