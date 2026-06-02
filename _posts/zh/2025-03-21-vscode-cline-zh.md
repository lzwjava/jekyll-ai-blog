---
audio: false
generated: true
lang: zh
layout: post
title: 在VSCode中使用Cline
translated: true
type: note
---

### 核心要点
- Cline 似乎可通过安装扩展在 VSCode 中使用，创建账户后即可通过自然语言提示进行交互。
- 研究表明配置 API 提供商（如 OpenRouter）可增强功能，需要提供 API 密钥。
- 现有证据倾向于 Cline 支持代码生成和终端命令等高级功能，并可选配特定模型。

---

### 安装与设置
要在 VSCode 中使用 Cline，请先确保已从[官网](https://code.visualstudio.com)安装 VSCode。然后打开 VSCode，进入扩展视图（点击扩展图标或按 Windows/Linux 的 `Ctrl+Shift+X` 或 macOS 的 `Cmd+Shift+X`），搜索 "Cline" 并点击"安装"。安装完成后，在活动栏点击 Cline 图标或使用命令面板（`Ctrl+Shift+P` 或 `Cmd+Shift+P`）打开 Cline，接着在 [app.cline.bot](https://app.cline.bot) 创建账户登录，初始会赠送免费额度且无需绑定信用卡。

### 使用 Cline
设置完成后，在聊天窗口输入自然语言提示与 Cline 交互，例如"生成一个数组排序函数"或"创建名为 'hello-world' 的新项目文件夹，内含显示蓝色大字 'Hello World' 的简单网页"。Cline 能生成代码、解释代码、调试错误，甚至在获得许可后执行终端命令（如安装包）。由于 AI 建议可能偶有错误，应用更改前请务必审核所有修改。

### 配置 API 提供商
为增强功能，可配置 OpenRouter 等 API 提供商。从 [OpenRouter.ai](https://openrouter.ai) 获取 API 密钥后，在 Cline 设置中输入基础 URL（如 `https://openrouter.ai/api/v1`）和模型 ID（如 `deepseek/deepseek-chat`），并粘贴 API 密钥。这样可访问特定模型以提升性能，但此为可选步骤，因 Cline 默认已内置可用模型。

---

---

### 调研笔记：VSCode 中使用 Cline 的完整指南

本节基于截至 2025 年 3 月 21 日的最新网络调研，对 AI 编程助手 Cline 在 Visual Studio Code (VSCode) 中的安装、设置、使用及高级配置进行详细剖析，在直接答案基础上展开全面审查。

#### Cline 与 VSCode 集成的背景
Cline 是一款开源 AI 编程助手，通过在 VSCode 内提供代码生成、调试和终端命令执行等功能来提升开发者效率。它支持多种 AI 模型，并可配置不同 API 提供商，是 GitHub Copilot 等工具的可扩展替代方案。用户可通过自然语言提示与 Cline 交互，它还能通过自定义指令和设置适应项目特定需求。

#### 分步安装与设置指南
按照以下详细步骤在 VSCode 中开始使用 Cline：

1. **安装 VSCode**：
   - 从官方网站下载并安装 VSCode：[官网链接](https://code.visualstudio.com)。启动时若提示运行扩展请务必允许。

2. **安装 Cline 扩展**：
   - 打开 VSCode，通过点击活动栏的扩展图标或按 `Ctrl+Shift+X`（Windows/Linux）或 `Cmd+Shift+X`（macOS）进入扩展视图。
   - 在搜索栏输入 "Cline" 查找扩展。
   - 点击由 saoudrizwan 开发的 Cline 扩展旁的"安装"按钮，扩展位于 [VSCode 应用市场](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)。

3. **打开 Cline 文件夹**：
   - 为结构化设置，建议打开 Documents 目录中的 "Cline" 文件夹：
     - macOS：`/Users/[用户名]/Documents/Cline`
     - Windows：`C:\Users\\[用户名]\Documents\Cline`
   - 此步骤适用于项目组织，但基础使用中为可选。

4. **创建 Cline 账户并登录**：
   - 安装后，点击活动栏的 Cline 图标打开扩展，或使用命令面板（`Ctrl+Shift+P` 或 `Cmd+Shift+P`）输入 "Cline: Open In New Tab" 获得更佳视图。
   - 在 Cline 界面点击"登录"，将跳转至 [app.cline.bot](https://app.cline.bot) 创建账户。该过程初始赠送免费额度，无需信用卡，方便新用户使用。

#### 配置 API 提供商以增强功能
Cline 支持多种 API 提供商以利用不同 AI 模型，配置后可提升性能并访问特定模型。此过程为可选但推荐给需要高级功能的用户。设置方法如下：

- **支持的 API 提供商**：Cline 可与 OpenRouter、Anthropic、OpenAI、Google Gemini、AWS Bedrock、Azure、GCP Vertex 等提供商集成，也支持任何 OpenAI 兼容 API 或通过 LM Studio/Ollama 的本地模型。
- **配置步骤**：
  - 在 VSCode 中打开 Cline 扩展并访问设置（通常通过齿轮图标或 VSCode 设置菜单）。
  - 选择首选 API 提供商。例如使用 OpenRouter：
    - 从 [OpenRouter.ai](https://openrouter.ai) 获取 API 密钥，确保启用支出限制以控制成本。
    - 输入基础 URL：`https://openrouter.ai/api/v1`。
    - 指定模型 ID，如 DeepSeek Chat 的 `deepseek/deepseek-chat`。
    - 将 API 密钥粘贴到指定字段并保存设置。
  - 对于本地设置（如使用 Ollama）：
    - 从 [ollama.com](https://ollama.com) 安装 Ollama。
    - 拉取所需模型，例如 `ollama pull deepseek-r1:14b`，并在 Cline 中配置基础 URL `http://localhost:11434` 及对应模型 ID。

- **性能考量**：模型选择影响性能，具体取决于硬件。下表概述不同模型大小的硬件需求：

| **模型大小** | **所需内存** | **推荐 GPU**       |
|--------------|--------------|---------------------|
| 1.5B         | 4GB          | 集成显卡            |
| 7B           | 8–10GB       | NVIDIA GTX 1660     |
| 14B          | 16GB+        | RTX 3060/3080       |
| 70B          | 40GB+        | RTX 4090/A100       |

- **成本考量**：对于 OpenRouter 等云提供商，成本约为每百万输入令牌 0.01 美元，详细定价见 [OpenRouter 定价页](https://openrouter.ai/pricing)。使用 Ollama 的本地设置免费但需要足够硬件。

#### 使用 Cline 进行编程辅助
安装配置完成后，Cline 提供一系列功能辅助编程任务。以下为有效使用方法：

- **与 Cline 交互**：
  - 点击活动栏 Cline 图标或通过命令面板在新标签页打开 Cline 聊天窗口。
  - 输入自然语言提示请求帮助。示例如下：
    - "生成一个数组排序函数。"
    - "解释这段代码。"
    - "创建名为 'hello-world' 的新项目文件夹，制作显示蓝色大字 'Hello World' 的简单网页。"
  - 复杂任务请提供上下文（如项目目标或具体操作）以获得更准确回复。

- **高级功能**：
  - **代码生成与编辑**：Cline 可生成代码并编辑文件。使用如"请编辑 /path/to/file.js"或"@文件名"的命令指定文件。它会在差异视图中显示更改供审核后再应用，确保修改可控。
  - **终端命令执行**：Cline 可在用户许可下执行终端命令，如安装包或运行构建脚本。例如可询问"安装最新版 Node.js"，Cline 会在执行前确认。
  - **自定义指令**：在 Cline 设置中设定自定义指令以指导其行为，如强制编码标准、定义错误处理偏好或建立文档规范。这些指令可项目特定，并存储在项目根目录的 `.clinerules` 文件中。

- **审核与应用更改**：因 AI 生成代码可能看似合理实则有误，应用前请务必审核。Cline 的检查点系统允许在需要时回滚更改，确保进度可控。

#### 额外提示与最佳实践
为最大化 Cline 效用，请考虑以下建议：

- **提问技巧**：若不确认，直接在 Cline 聊天中输入查询，如"如何修复此错误？"提供额外上下文（如截图或复制的错误信息）可获得更好帮助。
- **使用限制与透明度**：Cline 跟踪整个任务循环及单个请求的总令牌数和 API 使用成本，让您知悉支出（尤其对云提供商非常实用）。
- **社区支持**：如需进一步帮助，可加入 Cline Discord 社区 [链接](https://discord.gg/cline)，查找故障排除指南并与其他用户交流。
- **模型选择**：根据需求选择模型，可选如 Anthropic Claude 3.5-Sonnet、DeepSeek Chat 和 Google Gemini 2.0 Flash 等选项，各自在编程任务中具有不同优势。

#### 意外细节：模型部署的灵活性
Cline 一个有趣之处是同时支持云和本地模型部署的灵活性。尽管多数用户可能认为云 AI 助手占主导，但 Cline 通过 Ollama 集成本地设置，可在硬件充足时提供免费、注重隐私的编程辅助。这种双重方法满足不同用户需求，从预算敏感的开发者到优先考虑数据安全的用户，尤其对开源爱好者相关。

#### 结论
总之，在 VSCode 中使用 Cline 涉及安装扩展、创建账户并通过自然语言提示交互获取编程辅助。配置 OpenRouter 等 API 提供商可通过访问特定模型增强功能，也可选配 Ollama 本地设置以节省成本。Cline 的代码生成、终端命令执行和自定义指令等高级功能使其成为开发者的强大工具，建议仔细审核 AI 生成输出。截至 2025 年 3 月 21 日，本指南提供了利用 Cline 提升编程效率的全面方法。

---

### 关键引用
- [Cline 官网新手入门指南](https://docs.cline.bot/getting-started/getting-started-new-coders)
- [Cline AI 自主编程助手 for VS Code](https://cline.bot/)
- [Cline GitHub 代码库](https://github.com/cline/cline)
- [如何在 VSCode 中使用 Cline 运行 DeepSeek R1](https://apidog.com/blog/free-deepseek-r1-vscode-cline/)
- [VSCode 应用市场 Cline 扩展](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
- [Cline Discord 社区](https://discord.gg/cline)
- [OpenRouter AI 平台](https://openrouter.ai)
- [Ollama 官网](https://ollama.com)
- [OpenRouter AI 定价](https://openrouter.ai/pricing)
