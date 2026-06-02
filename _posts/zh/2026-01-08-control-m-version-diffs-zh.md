---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Control-M 客户端 9.20 与 9.21 版本差异
translated: true
type: note
---

**Question:** Windows 上的 Control-M client v9.20 和 v9.21 之间有什么区别？

**Answer:**

Control-M (由 BMC 开发) 使用类似于 9.0.20 (通常简写为 9.20) 和 9.0.21 (9.21) 的版本命名规则，涵盖整个套件，包括 **Control-M/Enterprise Manager (EM)**、Server、Agent 以及 **desktop client** (Windows 上的 Control-M GUI client)。

Windows 上的 **Control-M client** 主要是来自 Control-M/EM 安装包的桌面应用程序。它连接到 EM/Server，并提供 Configuration Control Manager (CCM) 以及 Job 定义和监控界面等工具。

### 9.0.20 和 9.0.21 之间的主要区别 (与 Windows Client 相关)

- **Users 和 Roles 管理**: 在 9.0.21 中，用户权限和角色现在专门在 **Control-M Web** (基于浏览器的界面) 中进行管理。Control-M Configuration Manager (CCM，属于 desktop client 的一部分) 中的传统 Authorizations 工具已不再可用。对于以前使用 desktop client 进行权限管理的管理员来说，这是一个重大变化。

- **Compatibility 和 Connectivity**: 9.0.21 的 client 可以连接到较旧版本的 EM/Server (在兼容模式下最低可支持到 9.0.19)，但要访问 9.0.21 的新功能 (例如增强的 role-based access)，EM/Server 也必须升级。较旧的 client (9.0.20) 可以连接到 9.0.21 的 EM，但新功能的使用受限。

- **Installation 变化**: 9.0.21 中的 Control-M/EM 安装现在默认包含 SLA Management、Control-M/Forecast 和 Self Service 等额外组件。Windows 上的 client 安装可能会捆绑更多功能或更新的依赖项。

- **其他 Client 相关的增强**:
  - 改进了与 **Control-M Automation API** 的集成 (Secrets 保护、新的 Token 类型)。
  - 术语与 Helix Control-M 保持一致。
  - 通用的 bug 修复和安全性改进 (例如，防止升级后降级的密码加密更改)。

- **Desktop Client 本身没有重大的 UI 改版**: 核心 desktop client 界面保持相似，但许多新功能 (例如 Workflow Insights dashboards、Control-M for Airflow 等新插件) 主要集成在 Control-M Web 中，鼓励用户从 desktop client 转向 Web 端进行日常操作。

- **Windows 特定注意事项**: 除了常规的平台支持外，没有提到 Windows client 特有的区别。两个版本都支持 Windows，且 Agent 仅以 64-bit 运行。

总的来说，从 9.0.20 升级到 9.0.21 引入了 **现代化授权管理** (迁移到 Web 端)，并鼓励使用 Control-M Web 而非传统的 desktop client，同时在安全性、API 和插件方面增加了后端增强。

有关所有更改的详细列表 (包括修复的问题和整个套件的新功能)，请参阅 BMC 官方 release notes。

**References:**

- [What's New in Control-M 9.0.21](https://docs.bmc.com/docs/controlm/90201/what-s-new-in-control-m-9-0-21-1044383595.html)
- [Introducing Control-M 9.0.21 (Blog Summary)](https://www.dbi-services.com/blog/introducing-control-m-9-0-21/)
- [Control-M Compatibility for Version 9.0.21](https://docs.bmc.com/docs/controlm/90201/control-m-compatibility-for-version-9-0-21-1044383593.html)
- [What's New in Control-M 9.0.20](https://docs.bmc.com/docs/controlm/9020/what-s-new-in-control-m-9-0-20-900847340.html)
