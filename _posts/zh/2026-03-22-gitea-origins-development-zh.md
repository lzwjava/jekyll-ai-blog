---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gitea的起源与发展
translated: true
type: note
---

**问题：** Gitea 是谁开发的，特别是自托管版本？

**回答：**

## 起源：Gogs → Gitea

Gitea 并非从零开始。它是 2016 年 **Gogs** 的一个 fork。虽然 Gogs 是开源的，但其仓库由单一维护者控制。这种单一维护者瓶颈让希望更快开发和更开放治理模式的贡献者感到沮丧。

为了应对这些限制，Gitea 开发者于 **2016 年 11 月** fork 了 Gogs，创建了社区驱动的开发模式。Gitea 于 2016 年 12 月发布了官方 **1.0 版本**。

---

## 谁开发的

Gitea 背后的关键人物是：

- **Lunny Xiao** — Gitea 的原始核心开发者之一和维护者，此前参与过 Gogs。
- **Matti Ranta** — 另一位核心维护者。

在 **2022 年 10 月**，维护者 **Lunny Xiao** 和 **Matti Ranta** 创立了公司 **Gitea Limited**，目标是提供使用 Gitea 专有版本的托管服务，这些版本未作为开源发布。这一商业化举措在社区中引发了争议。

除了这些创始人之外，Gitea 采用社区驱动的开发模式，意味着它有来自世界各地的众多开源贡献者，而非单一所有者。

---

## 它是什么（自托管）

Gitea 是一个轻松、自托管的一体化软件开发服务。它包括 Git 托管、代码审查、团队协作、软件包注册表和 CI/CD。它类似于 GitHub、Bitbucket 和 GitLab。

项目的目标是提供最简单、最快速、最轻松的自托管 Git 服务设置方式。由于 Gitea 使用 **Go** 编写，它支持 Go 支持的所有平台和架构，包括 Linux、macOS 和 Windows 在 x86、amd64、ARM 和 PowerPC 架构上。

它是免费的、自托管的，并采用 **MIT license**，赋予用户完全控制、无限用户和仓库。

---

## Forgejo 分支（社区反应）

针对 **Gitea Limited** 的创立及其非开源专有版本，当时使用 Gitea 的主要 forge **Codeberg** 将 Gitea fork 为 **Forgejo**。Forgejo 现在是那些希望 100% 开放治理模式的人的流行纯社区驱动替代品。

---

## 总结表格

| 项目 | 详情 |
|---|---|
| 原 fork 自 | Gogs (2016 年 11 月) |
| 关键创始人 | Lunny Xiao, Matti Ranta |
| 语言 | Go + TypeScript |
| 许可证 | MIT |
| 公司 | Gitea Limited (2022 年创立) |
| 社区分支 | Forgejo (由 Codeberg) |

**参考资料：**

- [Gitea - Wikipedia](https://en.wikipedia.org/wiki/Gitea)
- [Gitea Official Documentation](https://docs.gitea.com/)
- [Gitea GitHub Repository](https://github.com/go-gitea/gitea)
