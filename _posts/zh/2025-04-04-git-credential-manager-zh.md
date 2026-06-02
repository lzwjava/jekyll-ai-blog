---
audio: false
generated: true
lang: zh
layout: post
title: 使用 Git 凭据管理器进行 Git Push
translated: true
type: note
---

**标题：使用 Git 凭证管理器和代理配置实现无缝 Git 推送**

**引言：**

将本地 Git 更改推送到远程仓库（如 GitHub）本应是一个顺畅的过程。然而，网络配置（尤其是在使用代理时）有时会使事情复杂化。在这篇文章中，我将分享成功将更改推送到我的 `lzwjava.github.io` 仓库的经验，重点介绍 Git 凭证管理器（GCM）和正确代理设置的作用。

**场景描述：**

我需要将更新推送到 GitHub 上的 `lzwjava.github.io` 仓库。我的系统配置了使用代理服务器，这最初导致了身份验证问题。

**采取步骤：**

1. **验证代理设置：**

    * 我首先使用 `git credential-manager` 命令确认了我的代理设置。该命令有帮助地显示了我当前的 HTTP 和 HTTPS 代理配置：

    ```bash
    git credential-manager
    ```

    * 输出显示：

    ```
    🚀 **检测到代理设置：**
      - HTTP_PROXY: http://127.0.0.1:7890
      - HTTPS_PROXY: http://127.0.0.1:7890
    ```

    * 这确认了我的代理设置被正确检测到。

2. **使用 GCM 登录 GitHub：**

    * 为确保 Git 具有正确的凭据，我使用 GCM 登录了我的 GitHub 账户：

    ```bash
    git credential-manager github login
    ```

    * 此命令打开了一个浏览器窗口，提示我向 GitHub 进行身份验证。成功验证后，GCM 安全地存储了我的凭据。

3. **验证 GitHub 账户：**

    * 为了确认我的 GitHub 账户已正确登录，我运行了以下命令。

    ```bash
    git credential-manager github list
    ```

    * 此命令显示了我的 GitHub 账户名。

4. **设置远程 URL：**

    * 然后我验证并设置了仓库的远程 URL：

    ```bash
    git remote set-url origin https://github.com/lzwjava/lzwjava.github.io.git
    ```

5. **推送更改：**

    * 最后，我将本地更改推送到远程仓库：

    ```bash
    git push
    ```

    * `git push` 命令成功上传了我的更改。

6. **GitHub 安全警报：**

    * 推送后，GitHub 显示了一个关于我仓库依赖项中存在漏洞的安全警报。这是一个重要的提醒，需要定期检查和解决安全问题：

    ```
    remote: GitHub 在 lzwjava/lzwjava.github.io 的默认分支上发现 3 个漏洞（2 个高危，1 个低危）。欲了解更多信息，请访问：
    remote:    https://github.com/lzwjava/lzwjava.github.io/security/dependabot
    ```

**关键要点：**

* **Git 凭证管理器 (GCM)：** GCM 通过安全存储凭据和处理身份验证工作流，简化了 Git 身份验证。
* **代理配置：** 在代理后面工作时，请确保您的 Git 环境已正确配置为使用代理。GCM 检测和使用代理设置的能力非常宝贵。
* **安全警报：** 密切关注来自 GitHub 的安全警报，以保护您的仓库安全。
* **命令行工具：** 命令行是管理 Git 仓库的强大工具。

**结论：**

通过使用 Git 凭证管理器并正确配置代理设置，我成功地将更改推送到了 GitHub。这次经历凸显了理解和管理 Git 身份验证及网络配置的重要性。希望本指南能帮助您简化 Git 工作流程。
