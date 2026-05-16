---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Visual Studio Code 1.120 亮点与特性
translated: true
type: note
---

## Visual Studio Code 1.120 — 发布概览

**发布日期：** 2026年5月13日

VS Code 1.120 将 Agents 窗口引入稳定版，改进了 BYOK 模型的可见性和控制能力，并新增了 Markdown 质量改进和 agent 安全功能。

---

## 🤖 Agents

### Agents 窗口现已稳定（预览版）

新的 Agents 窗口是你熟悉编辑器的伴侣——专为 agent 驱动开发而设计，提供了一个专用空间来探索、迭代和审查跨多个项目的任务，并在它们之间无缝切换。它让你选择 agent 框架，在远程机器上运行 agent，并按照你想要的方式配置环境——包括颜色主题、键绑定和扩展。

本版本中 Agents 窗口的主要改进：

- **首选项跨会话保留**——你在 agent 框架和隔离模式等下拉菜单中的最后选择会被保留。
- **轻松放弃更改**——可以直接从“更改”面板中放弃编辑。
- **同步上游更改**——文件面板上的同步按钮让你在 agent 启动前从基础分支拉取上游更改。
- **在最近会话之间导航**——标题栏左上角的箭头按钮让你在最近会话之间跳转。
- **每个窗口的设置覆盖**——你可以仅为 Agents 窗口覆盖特定的 VS Code 设置。

你可以通过 VS Code 标题栏中的 **"Open in Agents"** 按钮打开 Agents 窗口。

### Copilot CLI 插件自动发现

使用 GitHub Copilot CLI 安装的 agent 插件会被 VS Code 自动识别，因此只需一次 `copilot plugin install` 即可覆盖两个界面。之前，你必须在 VS Code 中单独安装相同的插件，或者将其路径添加到 `chat.plugins.paths` 设置中。

---

## 🧠 语言模型（BYOK 改进）

### BYOK 模型的准确 Token 使用量

聊天视图中的上下文窗口控制现在会显示 BYOK（自带密钥）模型的准确 token 使用量和百分比。以前，当你通过自己的 API 密钥（Anthropic、OpenAI 或其他）与模型聊天时，该控制总是显示 0% 和零 token 计数，因为 token 计算仅适用于内置模型。

### 配置 BYOK 推理模型的思考努力

你现在可以直接从聊天视图的模型选择器中配置 BYOK 推理模型的思考努力。所选的努力会在每个请求中转发给模型，让你在延迟、成本和回答质量之间进行权衡。这适用于兼容 OpenAI 的端点（OpenAI、xAI/Grok、OpenRouter 以及自定义 Azure OpenAI 部署）。Anthropic 模型已经支持此功能；现在控制在所有提供商之间保持一致。

### 按提供商组织的模型选择器

聊天视图中的模型选择器现在按提供商对模型进行分组，使你在拥有来自多个来源的模型时更容易找到所需的模型。最近使用的模型还会在模型名称旁边以灰色文本显示提供商名称，以便你快速区分来自不同提供商的同名模型。你还可以通过在聊天输入框中输入 `/models` 来快速访问模型。

---

## 💬 聊天增强

### 终端工具输出压缩（预览版）

来自 `git diff`、`ls -l` 和 `npm install` 等命令的终端长输出可能会占用模型上下文窗口的很大一部分。当你启用 `chat.tools.compressOutput.enabled` 设置时，VS Code 会在将这些命令的输出发送给模型之前对其进行后处理。大型未更改的 hunk 在 diff 中被折叠，lockfile 和快照 diff 被丢弃，`ls -l` 缩减为条目名称，`npm install` 的进度条、弃用警告和审计摘要被移除。

### 终端命令风险评估（实验性）

为了帮助你快速判断一个命令是否值得仔细检查，终端命令确认现在包含一个风险徽章，其中包含 AI 生成的命令功能说明。每个徽章显示三个级别之一：**安全**（绿色）——读取文件或打印输出，不做更改；**谨慎**（橙色）——修改工作区、安装包或通过网络发送数据；**仔细审查**（红色）——执行可能难以或无法撤消的操作，例如强制推送到远程或删除工作区外的文件。

---

## 📝 Markdown 改进

本版本新增了 Markdown diff 预览功能，允许开发者在查看 diff 时以渲染后的输出形式审查 Markdown 内容，而不是原始语法。

---

## 📊 总结表格

| 领域 | 功能 | 状态 |
|---|---|---|
| Agents | Agents 窗口 | 稳定预览版 |
| Agents | Copilot CLI 插件自动发现 | GA |
| 语言模型 | BYOK Token 使用量显示 | GA |
| 语言模型 | BYOK 思考努力 | GA |
| 语言模型 | 按提供商的模型选择器 | GA |
| 聊天 | 终端输出压缩 | 预览版 |
| 聊天 | 终端命令风险评估 | 实验性 |
| 编辑器 | Markdown Diff 预览 | GA |

参考链接：

- [Visual Studio Code 1.120 发布说明](https://code.visualstudio.com/updates/v1_120)
- [VS Code 发布归档](https://code.visualstudio.com/updates/archive)