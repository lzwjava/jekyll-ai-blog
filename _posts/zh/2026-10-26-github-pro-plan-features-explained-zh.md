---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub Pro 计划功能详解
translated: true
type: note
---

**问题：** GitHub Pro计划各项功能是什么意思？

**回答：**

以下是针对GitHub Pro计划所列出的每一项提供的通俗易懂的解释：

---

### ✅ 包含的功能

**1. Required Reviewers（在私有仓库中）**
您可以通过设置，强制要求一个或多个特定人员批准拉取请求后才能合并。在 Free 计划中，此功能仅适用于公共仓库。Pro 计划在私有仓库中也提供此功能。

**2. Protected Branches（在私有仓库中）**
您可以锁定重要分支（例如 `main`），限制任何人直接推送或合并，除非满足特定规则（如 CI 检查或必需审查）。同样，Free 计划仅对公共仓库提供此功能。

**3. Repository Insights（在私有仓库中）**
一个内置的分析仪表板，展示贡献者活动、提交频率、流量和代码频率图表——有助于跟踪私有仓库的项目健康状况。

**4. Wikis（在私有仓库中）**
附属于仓库的内置文档 Wiki（如同轻量级知识库），在私有仓库中解锁。Free 用户只能在公共仓库中使用 Wiki。

**5. Pages（在私有仓库中）**
GitHub Pages 允许您直接从仓库托管静态网站。Pro 计划允许您在私有仓库中使用此功能；Free 计划仅允许在公共仓库中使用。

**6. Code Owners（在私有仓库中）**
通过 `CODEOWNERS` 文件，您可以指定当某些文件或目录在 PR 中被修改时，自动将谁标记为必需审查者。在 Pro 计划中，私有仓库解锁此功能。

**7. 3,000 分钟 GitHub Actions**
GitHub Actions 是内置的 CI/CD 系统（自动运行测试、构建、部署）。Pro 计划每月提供 **3,000 分钟免费** 的 GitHub 托管运行器时间，而 Free 计划为 2,000 分钟。

**8. 2GB GitHub Packages 存储**
GitHub Packages 是一个包注册表（可以托管 npm、Docker、Maven 等包，与代码一同存放）。Pro 计划将存储上限提高到 **2 GB**，而 Free 计划为 500 MB。

**9. 180 核小时 Codespaces 计算**
GitHub Codespaces 是基于云的 VS Code 开发环境——您可以在浏览器中启动一台配置完整的机器。Pro 计划包含 **每月 180 核小时**（例如，在 2 核机器上约 90 小时，4 核机器上约 45 小时）。

**10. 20GB Codespaces 存储**
Pro 计划中，您的 Codespaces 环境可用的磁盘空间（存储文件、Docker 层等）为 **每月 20 GB**。

---

### ❌ 不包括的功能

**GitHub Copilot Pro**
Copilot（AI 代码补全/聊天助手）是一项 **单独的附加订阅**——它不包含在 GitHub Pro 账户计划中。截至 2026 年，Copilot Pro 在基础计划之上每月额外花费 $10，因此您需要单独购买。

---

### 快速汇总表

| 功能 | GitHub Free | GitHub Pro |
|---|---|---|
| Required reviewers | 仅公共 | ✅ 私有也可以 |
| Protected branches | 仅公共 | ✅ 私有也可以 |
| Wikis / Pages / Code Owners | 仅公共 | ✅ 私有也可以 |
| Actions 分钟 | 2,000/月 | 3,000/月 |
| Packages 存储 | 500 MB | 2 GB |
| Codespaces 计算 | 120 核小时 | 180 核小时 |
| Codespaces 存储 | 15 GB | 20 GB |
| Copilot | ❌（仅免费层） | ❌（付费附加） |

---

**参考资料：**
- [GitHub's Plans – GitHub Docs](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)
- [GitHub Copilot Pricing 2026](https://nocode.mba/posts/github-copilot-pricing)