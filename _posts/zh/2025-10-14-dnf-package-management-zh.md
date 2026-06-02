---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: RHEL中的DNF包管理
translated: true
type: note
---

### Red Hat Enterprise Linux 中的 DNF 简介

DNF（Dandified YUM）是 Red Hat Enterprise Linux（RHEL）中的主要软件包管理工具，从 RHEL 8 开始引入并延续至 RHEL 9。它作为旧版 YUM（Yellowdog Updater, Modified）工具的继任者，提供了更优的性能、更好的依赖关系解析以及对模块化内容的支持。在 RHEL 中，DNF 负责处理通过 RPM（Red Hat Package Manager）仓库分发的软件包的安装、更新和移除。它确保用户可以访问通过 RHEL 订阅管理的关键内容集，例如 BaseOS（用于核心操作系统功能）和 AppStream（用于用户空间应用程序、运行时和工具）。

DNF 的宗旨是在保持系统稳定性的同时简化软件生命周期管理。它允许管理员和用户同时处理传统的 RPM 软件包和现代化的模块化格式，其中语言或数据库等组件可以拥有多个并行版本（称为“流”），而不会破坏基础操作系统。

#### 主要特性
- **模块化内容支持**：管理模块（相关 RPM 的集合）、流（特定版本的仓库）和配置文件（针对特定用例预配置的软件包集合，例如 Web 服务器或开发环境）。
- **仓库处理**：支持搜索、启用/禁用仓库，并配置如 BaseOS、AppStream 及补充仓库等来源。
- **安装与更新**：在安装软件包、软件包组或整个模块时自动解析依赖关系；支持检查更新、升级特定软件包或整个系统。
- **移除与回滚**：安全移除软件，并提供事务历史以撤销更改。
- **自定义与自动化**：可通过 `/etc/dnf/dnf.conf` 配置文件进行排除项、插件或缓存设置；与 DNF Automatic 等工具集成以实现计划更新。
- **向后兼容性**：在 RHEL 中，`yum` 命令被别名为 `dnf`，方便从旧版本过渡。

入门基础命令包括使用 `dnf install <软件包>` 进行安装，`dnf update` 进行升级，以及 `dnf search <关键词>` 查找软件。如需更高级的用法，请参阅官方文档。

[Red Hat Enterprise Linux 9：使用 DNF 工具管理软件](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html-single/managing_software_with_the_dnf_tool/index)
