---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ubuntu 升级工具的优点与风险
translated: true
type: note
---

**问题：** `do-release-upgrade` 是升级 Ubuntu 的好工具吗？

**回答：**

根据您的日志输出，您正在从之前的 Ubuntu 版本（可能是 22.04 "Jammy"）升级到 **Ubuntu 24.04 LTS "Noble Numbat"**。以下是对 `do-release-upgrade` 的全面评估以及预期情况：

---

## 什么是 `do-release-upgrade`？

它是 Ubuntu 官方的就地发行版升级工具。Ubuntu 推荐在 Server 版本和 cloud images 上使用 `do-release-upgrade` 命令，因为它可以处理发行版之间有时需要的系统配置更改。

---

## 它“很好”吗？——诚实的评估

### ✅ 优点

- **官方且经过充分测试**：这是升级 Ubuntu 的标准方式，无需完全重新安装。
- **处理配置合并**：当您的自定义配置文件（如 `sshd_config`）与新默认值不同时，它会提示您选择保留还是替换。
- **内置 SSH 安全网**：如您的日志所示，它会在端口 **1022** 上启动一个额外的 SSH 守护进程——即使主 SSH 连接中断，您也可以通过备用端口重新连接。
- 在进行任何更改之前，`do-release-upgrade` 会先执行检查以验证系统是否准备好升级，并在继续前提供摘要。
- 对于相当标准的服务器设置，整个过程通常需要 20–30 分钟。

### ⚠️ 注意事项 / 风险

- **通过 SSH 运行有风险**：如您的日志明确警告的那样，如果 SSH 连接在升级过程中断开，恢复会变得更困难。该工具通过打开端口 1022 来缓解此问题，但您应该有控制台/恢复选项（如 VPS 提供商的 web 控制台或 IPMI）。
- **配置冲突需要注意**：您的旧自定义配置与新默认值之间可能存在合并冲突——例如，`sshd_config` 和 `journald.conf` 之间。您需要决定保留哪个版本。
- **第三方 PPA 会被禁用**：第三方软件仓库和 PPA 在发行版升级期间会被禁用。虽然从这些来源安装的软件不会被移除，但这是升级问题的最常见原因。
- **继承旧默认值**：就地升级意味着您可能会继承旧 OS 的安全性较低的默认值。例如，如果 SSH 配置了较旧的协议版本，升级不会自动强制执行更新的安全默认值。
- **需要磁盘空间**：发行版升级涉及下载数百个新软件包，可能达数 GB。确保有足够的空闲磁盘空间，并 dành 时间监控交互过程。

---

## 您正在升级到的版本（Ubuntu 24.04 Noble）

从 Ubuntu 22.04 升级到 24.04 的任何人都会继承过去 2 年积累的累积变更集，这些变更增强并扩展了桌面和服务器体验。

Ubuntu 24.04 LTS 是几乎所有服务器工作负载的推荐选择，提供 5 年支持期、广泛测试，以及与 Kubernetes、Docker 和 Ansible 等工具的广泛兼容性。

---

## 底线

`do-release-upgrade` 在大多数情况下 **可靠且稳固**——尤其是如果您有恢复备用方案（控制台访问、备份）。它并非“完美”——自定义 PPA、修改的配置以及镜像特定问题（如社区报告中提到的 `Missing Signed-By` 错误）等边缘情况可能需要在之后手动清理。但对于标准系统，它运行良好，并远优于从头手动重新安装。

---

**参考资料：**

- [Ubuntu Official Upgrade Guide](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/)
- [Real-world do-release-upgrade Experience (22.04 → 24.04)](https://waldenperry.com/ubuntu-do-release-upgrade-experience/)
- [5 Options for Ubuntu 20.04 EOL - In-place Upgrade Pros/Cons](https://www.dogsbody.com/blog/5-options-for-ubuntu-20-04-eol-in-april-2025/)
- [Ubuntu 24.04 LTS: 20 Major Changes](https://www.omgubuntu.co.uk/2024/04/ubuntu-24-04-lts-20-changes-to-look-out-for)
- [Ubuntu Release Cycles: LTS vs Interim](https://oneuptime.com/blog/post/2026-03-02-ubuntu-release-cycles-lts-vs-interim/view)