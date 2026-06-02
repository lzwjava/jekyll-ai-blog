---
audio: false
generated: true
lang: zh
layout: post
title: 安装和使用Gemini命令行工具
translated: true
type: note
---

以下是关于安装、设置和使用 **Google Gemini CLI** 的简明指南。Gemini CLI 是一款开源 AI 代理，可将 Gemini 的功能集成到您的终端中，用于编码、任务自动化等。本指南基于截至 2025 年 6 月 29 日的最新信息。[](https://github.com/google-gemini/gemini-cli)[](https://dev.to/auden/google-gemini-cli-tutorial-how-to-install-and-use-it-with-images-4phb)[](https://gemini-cli.click/)

---

## **Google Gemini CLI 指南**

### **什么是 Gemini CLI？**
Gemini CLI 是 Google 开发的一款开源命令行工具，它将 Gemini 2.5 Pro 模型（拥有 100 万 token 上下文窗口）的强大功能带到您的终端。它支持编码、调试、内容生成、任务自动化以及多模态任务（如图像和视频生成）。使用 Google 账户即可免费使用，并且可以与 Google 搜索和模型上下文协议（MCP）服务器等工具集成。[](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/)[](https://dev.to/auden/google-gemini-cli-tutorial-how-to-install-and-use-it-with-images-4phb)

---

### **先决条件**
- **Node.js**：版本 18 或更高。使用 `node -v` 检查。如果需要，请从 [nodejs.org](https://nodejs.org) 安装。
- **Google 账户**：免费访问 Gemini 2.5 Pro（60 次请求/分钟，1,000 次请求/天）所必需。[](https://medium.com/google-cloud/getting-started-with-gemini-cli-8cc4674a1371)[](https://dev.to/auden/google-gemini-cli-tutorial-how-to-install-and-use-it-with-images-4phb)
- （可选）**API 密钥**：如需更高限制或使用特定模型，请从 [Google AI Studio](https://aistudio.google.com) 生成一个。[](https://github.com/google-gemini/gemini-cli)
- （可选）**Docker**：用于 MCP 服务器集成（例如 GitHub 工具）。[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials.md)

---

### **安装**
有两种方式可以开始使用 Gemini CLI：

1. **全局安装**：
   ```bash
   npm install -g @google/gemini-cli
   gemini
   ```
   这将全局安装 CLI 并使用 `gemini` 命令运行。[](https://gemini-cli.click/)

2. **无需安装直接运行**：
   ```bash
   npx https://github.com/google-gemini/gemini-cli
   ```
   这无需安装即可直接运行 CLI，适合测试。[](https://www.bleepingcomputer.com/news/artificial-intelligence/google-releases-gemini-cli-with-free-gemini-25-pro/)

---

### **设置**
1. **启动 CLI**：
   - 在终端中运行 `gemini`。
   - 首次运行时，选择一个主题（例如 ASCII、暗色、亮色）并按 Enter。[](https://dev.to/auden/google-gemini-cli-tutorial-how-to-install-and-use-it-with-images-4phb)

2. **身份验证**：
   - 选择 **使用 Google 登录** 以获得免费访问（推荐大多数用户使用）。
   - 浏览器窗口将打开；使用您的 Google 账户登录。
   - 或者，使用 API 密钥：
     - 从 [Google AI Studio](https://aistudio.google.com) 生成一个密钥。
     - 将其设置为环境变量：
       ```bash
       export GEMINI_API_KEY=您的_API_密钥
       ```
     - 这对于更高限制或企业用途很有用。[](https://github.com/google-gemini/gemini-cli)[](https://dev.to/auden/google-gemini-cli-tutorial-how-to-install-and-use-it-with-images-4phb)

3. **导航到您的项目**：
   - 在项目的根目录中运行 `gemini`，以便为代码相关任务提供上下文。[](https://dev.to/proflead/gemini-cli-full-tutorial-2ab5)

---

### **基本用法**
Gemini CLI 在交互式读取-求值-输出循环（REPL）环境中运行。输入命令或自然语言提示即可与 Gemini 模型交互。以下是一些常见任务：

1. **代码解释**：
   - 导航到项目文件夹并运行：
     ```bash
     gemini
     ```
   - 提示：`解释这个项目的架构` 或 `描述 main.py 中的主要函数`。
   - CLI 会读取文件并提供结构化的解释。[](https://www.datacamp.com/tutorial/gemini-cli)

2. **代码生成**：
   - 提示：`用 HTML、CSS 和 JavaScript 创建一个简单的待办事项应用`。
   - CLI 会生成代码，并可根据请求保存到文件。[](https://dev.to/proflead/gemini-cli-full-tutorial-2ab5)

3. **调试**：
   - 粘贴错误消息或堆栈跟踪并询问：`这个错误是什么原因引起的？`。
   - CLI 会分析错误并建议修复方法，可能使用 Google 搜索获取额外上下文。[](https://ts2.tech/en/everything-you-need-to-know-about-google-gemini-cli-features-news-and-expert-insights/)

4. **文件管理**：
   - 提示：`按支出月份整理我的 PDF 发票`。
   - CLI 可以操作文件或转换格式（例如，将图像转换为 PNG）。[](https://github.com/google-gemini/gemini-cli)

5. **GitHub 集成**：
   - 使用 MCP 服务器执行 GitHub 任务（例如，列出问题）：
     - 在 `.gemini/settings.json` 中配置 GitHub MCP 服务器，并提供个人访问令牌（PAT）。[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials.md)
     - 提示：`获取 foo/bar 仓库中分配给我的所有未解决问题`。
   - 运行 `/mcp` 列出已配置的 MCP 服务器和工具。[](https://medium.com/google-cloud/getting-started-with-gemini-cli-8cc4674a1371)

6. **多模态任务**：
   - 使用 Imagen 或 Veo 等工具生成媒体：
     - 提示：`使用 Veo 创建一段关于猫在澳大利亚冒险的短视频`。[](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/)

---

### **主要特性**
- **上下文文件（GEMINI.md）**：在项目根目录中添加 `GEMINI.md` 文件，以定义编码风格、项目规则或偏好（例如，“对 JavaScript 使用 async/await”）。CLI 会使用此文件来提供定制化的响应。[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md)[](https://ts2.tech/en/everything-you-need-to-know-about-google-gemini-cli-features-news-and-expert-insights/)
- **内置工具**：
   - `/tools`：列出可用工具（例如，Google 搜索、文件操作）。[](https://dev.to/proflead/gemini-cli-full-tutorial-2ab5)
   - `/compress`：总结聊天上下文以节省 token。[](https://www.datacamp.com/tutorial/gemini-cli)
   - `/bug`：直接向 Gemini CLI GitHub 仓库提交问题。[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md)
- **非交互模式**：用于脚本编写，通过管道传递命令：
   ```bash
   echo "编写一个 Python 脚本" | gemini
   ```
  [](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/index.md)
- **对话记忆**：使用 `/save <标签>` 保存会话历史，并使用 `/restore <标签>` 恢复。[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md)
- **自定义配置**：
   - 编辑 `~/.gemini/settings.json` 进行全局设置，或在项目中的 `.gemini/settings.json` 进行本地设置。
   - 示例：设置 MCP 服务器或自定义主题。[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md)

---

### **提示与技巧**
- **从计划开始**：对于复杂任务，先要求制定计划：`为登录系统创建一个详细的实施计划`。这可以确保结构化的输出。
- **使用本地上下文**：在 `GEMINI.md` 中编码项目特定细节，而不是依赖 MCP 服务器，以获得更快、更可靠的响应。
- **调试**：使用 `DEBUG=true gemini` 启用详细日志记录，以获取详细的请求/响应信息。[](https://apidog.com/blog/google-gemini-open-code-cli/)
- **审查更改**：在批准之前（输入 `y` 确认），始终审查文件修改或命令。[](https://apidog.com/blog/google-gemini-open-code-cli/)
- **探索工具**：运行 `/tools` 以发现内置功能，如网络搜索或保存记忆。[](https://dev.to/proflead/gemini-cli-full-tutorial-2ab5)

---

### **故障排除**
- **身份验证问题**：确保您的 Google 账户或 API 密钥有效。使用 `/auth` 切换方法。[](https://www.datacamp.com/tutorial/gemini-cli)
- **速率限制**：免费层级允许 60 次请求/分钟和 1,000 次/天。如需更高限制，请使用 API 密钥或 Vertex AI。[](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/)
- **错误**：查看 GitHub 上的[故障排除指南](https://github.com/google-gemini/gemini-cli/docs/troubleshooting.md)。[](https://github.com/google-gemini/gemini-cli)
- **响应缓慢**：CLI 处于预览阶段，进行 API 调用时可能较慢。请在 GitHub 上提交反馈。[](https://www.datacamp.com/tutorial/gemini-cli)

---

### **高级用法**
- **MCP 服务器集成**：
  - 设置 GitHub MCP 服务器以进行仓库交互：
    - 创建一个具有必要范围的 GitHub PAT。
    - 添加到 `.gemini/settings.json`：
      ```json
      {
        "mcpServers": [
          {
            "name": "github",
            "url": "http://localhost:8080",
            "type": "github"
          }
        ]
      }
      ```
    - 为 MCP 服务器运行 Docker 容器（参见 GitHub 文档）。[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials.md)
- **脚本编写**：通过将 Gemini CLI 集成到脚本来自动化任务：
  ```bash
  gemini --non-interactive "生成一个用于备份文件的 bash 脚本"
  ```
  [](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/index.md)
- **多模态提示**：
  - 示例：`描述这张图片：path/to/image.jpg`（需要支持视觉的模型，如 `gemini-pro-vision`）。[](https://github.com/eliben/gemini-cli)

---

### **限制**
- **预览阶段**：Gemini CLI 处于正式发布前阶段，可能存在支持有限或错误的情况。[](https://cloud.google.com/gemini/docs/codeassist/gemini-cli)
- **非完全开源**：只有 CLI UI 是 Apache 2.0 许可；Gemini 模型是专有的。[](https://www.bleepingcomputer.com/news/artificial-intelligence/google-releases-gemini-cli-with-free-gemini-25-pro/)
- **配额共享**：如果使用 Gemini Code Assist，限制是共享的。[](https://developers.google.com/gemini-code-assist/docs/gemini-cli)
- **未来定价**：预览期后的定价尚不明确；高级功能可能需要付费。[](https://ts2.tech/en/everything-you-need-to-know-about-google-gemini-cli-features-news-and-expert-insights/)

---

### **资源**
- **官方 GitHub**：[github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)[](https://github.com/google-gemini/gemini-cli)
- **文档**：[gemini-cli.click](https://gemini-cli.click) 或 GitHub 文档[](https://gemini-cli.click/)
- **博客公告**：[blog.google](https://blog.google)[](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/)
- **反馈**：在 GitHub 上提交错误或建议。[](https://ts2.tech/en/everything-you-need-to-know-about-google-gemini-cli-features-news-and-expert-insights/)

---

### **示例工作流程**
1. 安装：`npm install -g @google/gemini-cli`
2. 运行：`cd my-project && gemini`
3. 身份验证：使用 Google 登录。
4. 提示：`编写一个使用 FastAPI 的 REST API Python 脚本`。
5. 审查并保存生成的代码。
6. 使用 `/tools` 探索其他功能，如 GitHub 集成。

---

Gemini CLI 是一款功能强大的开发人员工具，可在终端中无缝集成 AI。从简单的任务开始，利用 `GEMINI.md` 提供上下文，并探索其多模态功能以提高生产力。更多示例，请查看 [GitHub 教程](https://github.com/google-gemini/gemini-cli/docs/cli/tutorials.md)。[](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials.md)

如果您需要具体示例或对特定功能有疑问，请告诉我！
