---
audio: false
generated: true
lang: zh
layout: post
title: 在Ubuntu上安装Outline客户端
translated: true
type: note
---

是的，您可以在 Ubuntu 上安装 Outline Client，因为它是基于 Debian 的 Linux 发行版，而 Outline Client 以 Debian 软件包的形式提供，与 Ubuntu 兼容。有两种安装方法：推荐的使用软件仓库的方法，以及直接下载 Debian 软件包的替代方法。下面，我将解释如何使用推荐的软件仓库方法进行操作，这种方法更可取，因为它与 Ubuntu 的软件包管理器集成，使得更新管理更加容易。

### 在 Ubuntu 上安装 Outline Client 的步骤（推荐方法）

按照以下步骤在您的 Ubuntu 系统上安装 Outline Client：

1. **打开终端**
    启动您 Ubuntu 系统上的终端应用程序。您可以通过在应用程序菜单中搜索“Terminal”或按 `Ctrl + Alt + T` 来执行此操作。

2. **安装 Outline 的软件仓库密钥**
    运行以下命令，将软件仓库的签名密钥下载并添加到系统的受信任密钥中。这可以确保来自该软件仓库的软件包经过真实性验证：

    ```bash
    wget -qO- https://us-apt.pkg.dev/doc/repo-signing-key.gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/gcloud-artifact-registry-us.gpg
    ```

3. **添加 Outline Client 软件仓库**
    通过运行以下命令，将 Outline Client 软件仓库添加到系统的源列表中。这会告诉 Ubuntu 在哪里可以找到 Outline Client 软件包：

    ```bash
    echo "deb [arch=amd64] https://us-apt.pkg.dev/projects/jigsaw-outline-apps outline-client main" | sudo tee /etc/apt/sources.list.d/outline-client.list
    ```

    - 注意：`[arch=amd64]` 部分指定这是用于 64 位系统。大多数现代 Ubuntu 安装都是 64 位的，但您可以通过运行 `uname -m` 来确认您系统的架构。如果输出是 `x86_64`，则表示您使用的是 64 位系统，此命令将按原样工作。

4. **更新软件包列表**
    刷新系统的软件包列表以包含新添加的 Outline 软件仓库：

    ```bash
    sudo apt update
    ```

5. **安装 Outline Client**
    使用以下命令安装最新版本的 Outline Client：

    ```bash
    sudo apt install outline-client
    ```

### 安装后

- **启动 Outline Client**：安装后，您可以在应用程序菜单中找到 Outline Client，或者通过在终端中输入 `outline-client` 来启动它。
- **保持更新**：要检查并安装更新，请使用 Ubuntu 的标准更新命令：

  ```bash
  sudo apt update
  sudo apt upgrade
  ```

  这些命令将更新所有已安装的软件包，包括 Outline Client，因为它通过软件仓库进行管理。请注意，从 1.15 版本开始，Linux 版 Outline Client 的应用内自动更新功能已被禁用，因此依赖软件包管理器是保持最新的最佳方式。
- **卸载**：如果您需要移除 Outline Client，请运行：

  ```bash
  sudo apt purge outline-client
  ```

### 为什么使用推荐的方法？

推荐使用软件仓库方法，因为：

- 它与 Ubuntu 的 `apt` 软件包管理器集成，允许您与其他系统软件包一起更新 Outline Client。
- 您无需手动下载和安装新版本，这与替代方法不同，在替代方法中，您需要为每次更新重复下载和安装过程。

### 假设与要求

- **Ubuntu 版本**：说明中未指定最低 Ubuntu 版本，但由于 Ubuntu 基于 Debian 且软件包针对 64 位系统，任何近期的 64 位 Ubuntu 版本都应该可以工作。为保险起见，请在开始之前通过运行 `sudo apt update && sudo apt upgrade` 确保您的系统是最新的。
- **架构**：这些说明假设是 64 位系统。如果您使用不同的架构（例如 32 位或 ARM），则此方法将无法按描述工作，您需要查找替代软件包或联系 Outline 支持。

### 替代方法（可选）

如果您不想添加软件仓库，可以直接下载并安装 Debian 软件包：

1. 下载软件包：

    ```bash
    wget -O ./outline-client.deb https://s3.amazonaws.com/outline-releases/client/linux/stable/outline-client_amd64.deb
    ```

2. 安装它：

    ```bash
    sudo apt install ./outline-client.deb
    ```

但是，您需要为更新手动重复此过程，这不太方便。

### 结论

使用推荐的软件仓库方法，您可以轻松地在 Ubuntu 上安装和维护 Outline Client。只需按照上述步骤操作，您就可以启动并运行它，并且能够通过系统的软件包管理器轻松地保持其更新。
