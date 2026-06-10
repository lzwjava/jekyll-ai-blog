---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Desktop 登录与模式
translated: true
type: note
---

问题：如何在 macOS 上通过电子邮件链接流程登录 Claude 桌面应用？Cowork、Claude Code 和 chat 是否真的都捆绑在同一个应用中？

回答：

这里涉及两个独立的问题。让我分别说明。

**1. macOS 上的电子邮件魔法链接登录**

是的，该流程可行。步骤如下：

1. 打开 Claude 桌面应用 → 点击 **继续使用电子邮件**。
2. 输入你的电子邮件 → Claude 发送一个登录链接。
3. 打开你的邮件客户端，点击链接 → 它会在默认浏览器中打开。
4. 浏览器完成身份验证，然后通过 `claude://` 深度链接将控制权交回应用（macOS 会提示“在 Claude 中打开？”→ 允许）。

浏览器到应用的跳转就是深度链接重定向。如果没有自动跳回，通常是因为 (a) 链接在与你当前登录会话不一致的浏览器中打开，或者 (b) 深度链接处理器未注册。解决方法是：复制链接并直接粘贴，或者直接使用**继续使用 Google**，这完全跳过了电子邮件往返过程。

**2. “Cowork、Claude Code、chat 都在同一个应用中”——部分正确**

让我验证当前状态，而不是猜测，因为桌面应用的界面一直在变化。确认。你的理解两部分都是正确的。

**登录流程：** 电子邮件魔法链接完全按你描述的方式工作——在应用中输入电子邮件，在邮件客户端中点击链接，浏览器进行身份验证，然后通过深度链接返回应用。如果你想跳过往返过程，Google SSO 是更快的途径。

**一个应用，多种模式：** 是的。Claude 桌面应用在界面顶部有三个主要模式：Chat（经典对话，类似于网页版）、Cowork（在你的文件上工作的自主代理）和 Claude Code 访问。你可以通过顶部的模式选择器/选项卡进行切换。

鉴于你的设置，有几个值得了解的细节：

- Cowork 在你计算机上的沙盒虚拟机中运行，这使其无法修改系统文件或未经允许访问沙盒之外的任何内容。启动虚拟机正是 Cowork 比 Chat 更重的原因——这与你的 16GB M2 Air 相关。对于真正的代理式文件操作，你可能会感受到 RAM 压力；位于 `<IP_ADDRESS>`（62GB）的工作站是更好的主机，如果你能在那里运行桌面应用的话。
- Claude Code 是 CLI 编码代理（编写代码、运行测试、提交 PR、从终端管理仓库）；Cowork 位于桌面应用内部，是 Anthropic 发现开发者将 Claude Code 用于远超编码的用途后引入的。两者现在共享相同的计算机使用能力。
- 需要付费计划——每月 20 美元的 Pro 计划现在包含 Chat、Cowork 和 Claude Code 访问权限；免费版不包含。
- 默认模型在重负载层级是 Opus 4.8，在日常层级是 Sonnet 4.6。

由于你优先使用终端（Warp）并且快速进行 vibe-coding，Claude Code 是你的自然入口点，而 Cowork 是图形化文件自动化层，你较少会用到。

参考链接：

- [Claude Desktop explained: chat, Cowork and Code](https://www.clickforest.com/en/blog/claude-desktop-explained)
- [Claude Code Can Now Run Your Desktop — DevOps.com](https://devops.com/claude-code-can-now-run-your-desktop/)
- [Claude Desktop System Requirements 2026 — Houtini](https://houtini.com/articles/claude-desktop-system-requirements/)