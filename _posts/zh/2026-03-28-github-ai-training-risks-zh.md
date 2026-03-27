---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GitHub AI 训练数据的风险
translated: true
type: note
---

**Question:** 启用“允许 GitHub 使用我的数据进行 AI 模型训练”是一个坏主意吗 —— 这会导致像 API key 泄露之类的事情吗？

**Answer:**

是的，你的担忧完全是有道理的。这个设置确实存在风险，security researchers 已经记录了现实世界中的后果。以下是详细分析：

---

## 这个设置到底在做什么？

如果你使用的是 GitHub Copilot Free、Pro 或 Pro+，启用此选项意味着你的交互数据 —— 包括你正在处理的任何内容的 snippets（包括 private repositories）—— 都会流入 AI 训练流水线。

这涵盖了你的文件结构、命名规范、comments 以及你在代码库中的导航方式。对于任何从事 proprietary software 开发的人来说，这意味着公司的 intellectual property 正在流入训练流水线。

---

## 是的，API keys 和 secrets 确实会泄露 —— 方式如下：

### 1. 直接训练数据暴露
如果 developer 在 script 中硬编码了 API key，一旦进入 Copilot 的训练过程，它就可能变得容易被暴露。此外，一旦 key 被嵌入到训练数据中，仅仅从 repository 中识别并删除 secret 已不足以防止泄露 —— 它仍会被模型记住。

### 2. 本地文件上下文（甚至包括 `.env` 文件！）
Copilot 会处理工作目录（working directory）中的任何内容。目前没有内置机制可以排除敏感文件。如果你在项目中有 API keys、database credentials 或 secrets —— 即使它们位于被 gitignore 的 `.env` 文件中 —— Copilot 在活动期间仍然可以看到它们，因为它读取的是你的本地文件，而不只是 git 中的内容。

### 3. 已证实的 Secret 泄露率
GitGuardian 的研究发现，在抽样的约 20,000 个激活了 Copilot 的 repositories 中，超过 1,200 个泄露了至少一个 secret —— 发生率为 6.4%，这比在所有 public repositories 中观察到的比例高出 40%。

### 4. 模型可以向其他用户复现 Secrets
研究结果表明，这些模型不仅会泄露其训练数据中存在的原始 secrets，还会建议在训练語料库其他地方遇到的其他 secrets —— 从而将敏感信息暴露给完全不同的用户。

### 5. 真实漏洞：CamoLeak Vulnerability
一个被称为 CamoLeak 的严重漏洞（CVSS 评分 9.6）允许攻击者在 pull requests 内部不可见的 markdown comments 中隐藏恶意 prompts，诱导 Copilot Chat 在 repo 中搜索 API keys 和 tokens，然后通过隐蔽的图像加载通道（image-loading channel）逐个字符地外泄数据。GitHub 随后修补了这个特定的 attack vector，但它说明了暴露程度可能有多严重。

---

## Free vs. Enterprise：巨大的差异

GitHub Copilot 的隐私控制在 Business 和 Enterprise 层级中更加健壮，提供了诸如阻止与公共代码匹配的建议、content exclusion 以及 audit logging 等功能。Free 层级可能会使用用户交互来进行模型改进，因此不建议用于 proprietary 或受监管的代码。

然而，即使是 Business/Enterprise 也存在缺口：如果一名个体 developer 使用个人的 Copilot Free 账户向企业 repo 贡献代码，即使公司拥有 enterprise 保护措施，该交互数据仍可能进入训练流水线。

---

## 你应该怎么做

1. **立即禁用该设置** —— 前往 `Settings > Copilot > Privacy` 并关闭用于 AI 训练的数据共享。
2. **切勿硬编码 secrets** —— 使用 environment variables 或 secrets manager（例如 HashiCorp Vault, AWS Secrets Manager）。
3. **使用 secrets scanning 工具** —— 像 GitGuardian 或 TruffleHog 这样的工具可以在 exposed credentials 扩散之前检测到它们。
4. **如果代码涉及商业机密或客户，请升级到 Business/Enterprise** —— free/personal 层级的保护措施最弱。
5. **将所有 AI 生成的代码视为不可信** —— 在 commit 之前进行审查，特别是检查是否存在硬编码的 credentials。

---

**底线：** 你的直觉是正确的。默认不退出（opt-out）的设计是针对那些从不检查隐私设置的大多数用户。如果你正在处理任何稍微敏感的内容 —— 客户代码、proprietary systems 或任何带有 credentials 的内容 —— **请保持该开关关闭（OFF）**。

**References:**

- [GitHub Copilot Security Risks (Prompt Security)](https://prompt.security/blog/securing-enterprise-data-in-the-face-of-github-copilot-vulnerabilities)
- [GitHub Copilot Privacy: Key Risks and Best Practices (GitGuardian)](https://blog.gitguardian.com/github-copilot-security-and-privacy/)
- [Yes, GitHub Copilot Can Leak Real Secrets (GitGuardian)](https://blog.gitguardian.com/yes-github-copilot-can-leak-secrets/)
- [GitHub Copilot Is Training on Your Private Code Now (DEV Community)](https://dev.to/alanwest/github-copilot-is-training-on-your-private-code-now-you-probably-didnt-notice-2f6)
- [CamoLeak Vulnerability (The Register)](https://www.theregister.com/2025/10/09/github_copilot_chat_vulnerability/)
- [GitHub Copilot Security Risks for Enterprises (MintMCP)](https://www.mintmcp.com/blog/github-copilot-security-risks)