---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 配置Hermes代理工具菜单
translated: true
type: note
---

**问题：** 如何在 Hermes Agent 中使用工具配置菜单（包含 Exa API 密钥、Firecrawl、Tavily、Browserbase 等选项）？

**回答：**

Hermes Agent（由 Nous Research 开发）提供交互式设置系统，用于配置其众多内置工具，这些工具扩展了代理的能力，例如网络搜索、内容提取、浏览器自动化、图像生成、文本转语音、记忆等。

您看到的菜单是交互式配置界面的一部分（可能在运行 `hermes setup`、`hermes tools` 或启用特定工具集时显示）。以下是逐步使用和配置的方法：

### 1. **访问工具配置**
- 在终端中运行以下命令之一（安装 Hermes Agent 后）：
  - `hermes setup` → 完整的交互式向导（推荐首次设置；包含模型和工具）。
  - `hermes tools` → 专门用于启用/禁用和配置工具。
  - `hermes setup tools` → 针对性的工具设置。
- 使用方向键（`↑ ↓`）浏览选项。
- 按 **空格键** 切换复选框（`[ ]` → `[x]`）。
- 按 **回车键** 确认选择。
- 按 **ESC 键** 取消/返回。

### 2. **各选项的功能**
所列项目是不同工具后端的 API 密钥和设置：

- **网络搜索与提取工具**：
  - Exa API 密钥 → 为 AI 原生网络搜索/提取提供支持（替代后端）。
  - Parallel API 密钥 → 另一个 AI 原生搜索/提取选项。
  - Firecrawl API 密钥 → 用于网络搜索、抓取和爬取（强烈推荐以获得稳定性能）。
  - Firecrawl API URL → 可选；用于**自托管**的 Firecrawl 实例（例如 `http://localhost:3002`），而非云服务。
  - Tavily API 密钥 → AI 原生搜索、提取和爬取。

- **浏览器自动化**：
  - Browserbase API 密钥 / 项目 ID → 云浏览器支持。
  - Browser Use API 密钥 → 替代云浏览器后端。
  - Firecrawl 浏览器会话 TTL → 浏览器会话的超时设置（默认：300 秒）。
  - Camofox 浏览器服务器 URL → 用于本地反检测浏览（例如 `http://localhost:9377`）。

- **其他工具**：
  - FAL API 密钥 → 图像生成。
  - Tinker API 密钥 → RL（强化学习）训练。
  - Weights & Biases API 密钥 → RL 实验跟踪。
  - OpenAI API 密钥 → 语音转录（Whisper）和文本转语音。
  - ElevenLabs API 密钥 → 高级文本转语音音色。
  - GitHub token → 更高的速率限制以及在 Skills Hub 发布技能。
  - Honcho API 密钥 / Base URL → AI 原生持久记忆（提供自托管选项）。

启用后，界面通常会提示您粘贴相应的 API 密钥或 URL。

### 3. **配置如何保存**
- **API 密钥和秘密**会自动保存到 `~/.hermes/.env`（安全，仅所有者可访问）。
- **非秘密设置**（例如启用的工具、后端）保存到 `~/.hermes/config.yaml`。
- 您也可以手动设置值：
  ```bash
  hermes config set FIRECRAWL_API_KEY fc-YourKeyHere
  hermes config set FIRECRAWL_API_URL http://localhost:3002
  ```
- 对于网络搜索后端偏好，可以在 `config.yaml` 中的 `web: backend: firecrawl`（或 `tavily`、`exa` 等）下配置。

### 4. **推荐的快速设置流程**
1. 运行 `hermes setup` 或 `hermes tools`。
2. 启用您需要的工具（建议从 Firecrawl 或 Tavily 开始以支持网络功能——它们非常可靠）。
3. 在提示时粘贴您的 API 密钥。
4. 对于自托管选项（例如本地 Firecrawl 或 Camofox），提供本地 URL 而非云密钥。
5. 确认并退出——Hermes 将在下次运行时加载工具。

### 5. **提示**
- 您无需启用每个工具。从最小化开始（例如一个网络搜索后端 + 记忆）以避免不必要的依赖。
- 许多工具可与本地模型（通过 Ollama、vLLM 等）开箱即用。
- 配置后，通过与代理聊天（CLI 或通过 Telegram/Discord 集成）并让其执行网络相关任务来进行测试。
- 完整文档请参考 Hermes Agent 官方文档中关于工具和配置的部分。

此设置使 Hermes Agent 具有高度可扩展性，而无需编写自定义代码。

**参考：**
- [Tools & Toolsets | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools/)
- [Configuration | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/)
- [Environment Variables Reference](https://mintlify.com/NousResearch/hermes-agent/reference/environment-variables)
- [GitHub README - Hermes Agent](https://github.com/NousResearch/hermes-agent/blob/main/README.md)
