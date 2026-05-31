---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 切勿在GitHub仓库中存储API密钥
translated: true
type: note
---

**问题：** 在私有 GitHub 仓库中存储 OpenAI、Anthropic、OpenRouter 及其他 LLM 提供商的 API 密钥或令牌是否安全？

**答案：**

**不安全。请勿将 API 密钥存储在任何 GitHub 仓库中，无论是私有的还是公开的。**

以下是"私有"并非安全边界的原因：

## 为什么私有仓库不安全

1. **意外的可见性变更** — 一次错误的点击就可能将私有仓库变为公开。GitHub 历史上曾因 UI 混淆导致此类问题。
2. **协作者访问权限** — 你添加的任何仓库协作者都能获取密钥。这是扁平化的访问模型，没有精细的权限控制。
3. **GitHub 自身** — GitHub 会扫描仓库（包括私有仓库），且曾发生过安全漏洞。根据服务条款，GitHub 员工可以访问私有仓库。
4. **分支与克隆** — 协作者可以创建分支或克隆仓库，导致你的密钥存储在他们的本地设备上。
5. **Git 历史永久留存** — 即使从文件中删除了密钥，它仍会保留在 `git log` 中。需要使用 `git filter-branch` 或 BFG 工具才能清除。
6. **CI/CD 暴露风险** — GitHub Actions 日志、第三方 Actions 或配置错误的工作流可能导致私有仓库中的密钥泄露。
7. **令牌泄露风险** — 如果您的 GitHub 个人访问令牌（PAT）被泄露，攻击者将能看到您所有的私有仓库及其中的所有密钥。

---

## 正确做法：密钥管理

### 本地开发（您的 MacBook / 工作站）

```bash
# ~/.zshrc 或 ~/.bashrc — 不要放在任何仓库中
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENROUTER_API_KEY="sk-or-..."
```

在代码中加载：

```python
import os
key = os.environ["ANTHROPIC_API_KEY"]
```

### 按项目：`.env` 文件

```bash
# .env  ← 已被 git 忽略
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

```bash
# .gitignore
.env
.env.*
*.env
```

使用 `python-dotenv` 加载：

```python
from dotenv import load_dotenv
load_dotenv()
```

**在进行首次提交之前，务必将 `.env` 添加到 `.gitignore` 中。**

### 每次创建新仓库前检查您的 `.gitignore`

```bash
# 在 git add 之前验证 .env 是否已被忽略
git check-ignore -v .env
```

### 生产环境 / CI

| 场景 | 工具 |
|---|---|
| GitHub Actions | [加密密钥](https://docs.github.com/en/actions/security-guides/encrypted-secrets)（通过 `设置 → 密钥`） |
| 任何云平台 | AWS Secrets Manager、GCP Secret Manager、Azure Key Vault |
| 自托管 | HashiCorp Vault |
| 团队密钥管理 | 1Password Secrets Automation、Doppler |

---

## 如果您已经提交了密钥

假设密钥已被泄露。存储在 Git 历史中的密钥实际上已公开。

1. **立即撤销密钥** — 前往 OpenAI/Anthropic/OpenRouter 后台删除它
2. **生成一个新密钥**
3. **如有必要，清除历史记录**（使用 BFG Reaper 或 `git filter-repo`）

```bash
# 安装 BFG
brew install bfg

# 从所有历史记录中清除特定字符串
bfg --replace-text secrets.txt my-repo.git
```

---

## 总结

| 存储方式 | 安全吗？ |
|---|---|
| 私有 GitHub 仓库 | ❌ 不安全 |
| 公开 GitHub 仓库 | ❌ 绝对不安全 |
| `~/.bashrc` / `~/.zshrc`（本地） | ✅ 本地开发可行 |
| `.env`（已加入 git 忽略） | ✅ 本地开发可行 |
| GitHub Actions 加密密钥 | ✅ CI 环境可行 |
| 云密钥管理器 | ✅ 生产环境最佳 |

根据您的设置（两台机器加 AMD 云），实用建议是：每台机器上使用 `~/.zshrc` 中的环境变量，为每个项目密钥使用带有完善 `.gitignore` 模板的 `.env` 文件，对于任何 CI/CD 流水线则使用 GitHub 加密密钥。