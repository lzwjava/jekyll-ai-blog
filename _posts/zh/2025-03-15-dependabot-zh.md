---
audio: false
generated: true
lang: zh
layout: post
title: 移除Dependabot
translated: true
type: note
---

要从 GitHub Actions 中移除 Dependabot，你需要禁用其创建触发工作流程的拉取请求功能，并可选择移除与 Dependabot 绑定的任何自定义工作流程。以下是实现此目标的步骤。请注意，我假设您查询中的 "dependant bot" 指的是 "Dependabot"，这是 GitHub 中用于依赖管理的常用工具。

---

### 步骤 1：禁用 Dependabot 版本更新
Dependabot 版本更新会自动创建拉取请求以保持依赖项最新。这些拉取请求可能触发 GitHub Actions 工作流程。要禁用此功能：

- **定位配置文件**：检查仓库中 `.github` 目录下是否存在名为 `dependabot.yml` 的文件。
- **删除文件**：如果该文件存在，请删除 `dependabot.yml` 文件并提交此更改。这将停止 Dependabot 为版本更新创建拉取请求。
- **验证**：如果不存在 `dependabot.yml` 文件，则版本更新功能已被禁用。

---

### 步骤 2：禁用 Dependabot 安全更新
Dependabot 安全更新会生成拉取请求以修复依赖项中的漏洞，这也可能触发 GitHub Actions 工作流程。要关闭此功能：

- **进入仓库设置**：在 GitHub 仓库中，点击 **Settings** 标签页。
- **导航至安全设置**：滚动到 **Security & analysis**（或 **Code security and analysis**，具体取决于您的 GitHub 界面）。
- **禁用安全更新**：找到 **Dependabot security updates** 并点击 **Disable**。

这将阻止 Dependabot 为安全修复创建拉取请求。

---

### 步骤 3：（可选）移除与 Dependabot 相关的自定义工作流程
如果您设置了专门处理 Dependabot 拉取请求的 GitHub Actions 工作流程（例如自动合并、标签管理或使用 Dependabot 元数据），您可能需要清理这些工作流程：

- **检查工作流程文件**：查看 `.github/workflows` 目录中的 YAML 文件。
- **识别 Dependabot 逻辑**：搜索条件语句，如 `if: github.event.pull_request.user.login == 'dependabot[bot]'`，或诸如 `dependabot/fetch-metadata` 之类的操作。
- **移除或修改**：删除这些工作流程或调整它们以移除 Dependabot 特定逻辑，然后提交更改。

此步骤是可选的，因为在步骤 1 和 2 中禁用 Dependabot 将阻止其创建新的拉取请求，这意味着现有工作流程将不再被 Dependabot 触发。但是，移除这些工作流程可以确保彻底清理。

---

### 补充说明
- **现有拉取请求**：禁用 Dependabot 不会关闭其已创建的现有拉取请求。如果这些请求被更新，仍可能触发工作流程。如有需要，您可以手动关闭它们。
- **Dependabot 警报**：如果您还想停止漏洞通知（与 GitHub Actions 无直接关联），请前往 **Settings > Security & analysis** 并禁用 **Dependabot alerts**。这是可选的，与工作流程触发器无关。

---

### 结果
完成步骤 1 和 2 后，Dependabot 将不再在您的仓库中创建拉取请求，从而有效“移除”其对 GitHub Actions 的影响。如果您为 Dependabot 自定义了工作流程，步骤 3 可确保所有相关自动化都被清除。您的 GitHub Actions 现在将仅基于其他事件运行，不受 Dependabot 影响。
