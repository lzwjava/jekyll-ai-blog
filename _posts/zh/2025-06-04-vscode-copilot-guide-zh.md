---
audio: false
generated: true
lang: zh
layout: post
title: 在 Visual Studio Code 中使用 GitHub Copilot
translated: true
type: note
---

GitHub Copilot 是由 GitHub 和 OpenAI 联合开发的 AI 编程助手，旨在提升开发者在 Visual Studio Code（VS Code）中的工作效率。它提供上下文感知的代码补全、自然语言对话和高级编辑功能。本指南将引导您完成 Copilot 的设置流程，探索其功能特性，并通过实用技巧和最佳实践优化工作流。

## 1. GitHub Copilot 简介

GitHub Copilot 如同一位 AI 结对编程伙伴，能够实时提供代码建议、解答编程问题并自动化重复性任务。其底层由基于海量公开代码库训练的大语言模型驱动，支持包括 Python、JavaScript、TypeScript、Ruby、Go、C# 和 C++ 在内的多种编程语言和框架。

核心功能包括：

- **代码补全**：在键入时推荐代码片段，从单行到完整函数均可覆盖
- **Copilot 对话**：通过自然语言查询解释代码、生成片段或调试问题
- **代理模式**：自动化多步骤编码任务（如重构代码或创建应用）
- **自定义指令**：根据编码风格或项目需求定制建议内容

## 2. 在 VS Code 中配置 GitHub Copilot

### 环境准备

- **VS Code**：从[官网](https://code.visualstudio.com/)下载安装，确保使用兼容版本（所有近期版本均支持 Copilot）
- **GitHub 账户**：需要具备 Copilot 访问权限的 GitHub 账户，可选方案：
  - **Copilot 免费版**：每月提供有限次数的补全和对话交互
  - **Copilot Pro/Pro+**：付费方案包含更高使用限额和高级功能
  - **组织访问**：若由组织提供，请向管理员咨询访问详情
- **网络连接**：Copilot 需保持在线状态才能提供建议

### 安装步骤

1. **启动 VS Code**：
   在计算机上打开 Visual Studio Code

2. **安装 GitHub Copilot 扩展**：
   - 进入**扩展**视图（Ctrl+Shift+X 或 macOS 的 Cmd+Shift+X）
   - 在扩展市场中搜索 "GitHub Copilot"
   - 点击官方 GitHub Copilot 扩展的**安装**按钮（将自动同步安装 Copilot 对话扩展）

3. **登录 GitHub**：
   - 安装后 VS Code 状态栏（右下角）可能出现设置提示
   - 点击 Copilot 图标并选择**登录**进行 GitHub 账户认证
   - 若无提示，可通过命令面板（Ctrl+Shift+P 或 Cmd+Shift+P）运行 `GitHub Copilot: Sign in` 命令
   - 按照浏览器认证流程，将 VS Code 提供的验证码复制到 GitHub

4. **验证激活状态**：
   - 登录成功后，状态栏的 Copilot 图标将转为绿色表示已激活
   - 若无 Copilot 订阅，将自动注册至每月有限使用的免费版

5. **可选：关闭遥测数据**：
   - 默认情况下 Copilot 会收集遥测数据，可在**设置**（Ctrl+, 或 Cmd+,）中搜索 `telemetry.telemetryLevel` 设为 `off`
   - 或通过 `GitHub Copilot Settings` 调整 Copilot 专属设置

> **注意**：若组织已禁用 Copilot 对话或限制功能，请联系管理员。故障排除请参阅 [GitHub Copilot 故障排除指南](https://docs.github.com/en/copilot/troubleshooting)。[](https://code.visualstudio.com/docs/copilot/setup)

## 3. GitHub Copilot 在 VS Code 中的核心功能

### 3.1 代码补全

Copilot 根据代码上下文和文件结构，在键入时推荐从单行到完整函数/类的代码建议

- **运行机制**：
  - 在支持的语言中开始键入（如 JavaScript、Python、C#）
  - Copilot 以灰色"幽灵文本"显示建议
  - 按 **Tab** 接受建议，继续键入则忽略
  - 使用 **Alt+]**（下一条）或 **Alt+[**（上一条）循环查看多个建议
- **示例**：

  ```javascript
  // 计算数字的阶乘
  function factorial(n) {
  ```

  Copilot 可能推荐：

  ```javascript
  if (n === 0) return 1;
  return n * factorial(n - 1);
  }
  ```

  按 **Tab** 接受建议

- **技巧**：
  - 使用描述性函数名或注释引导 Copilot（例如 `// 对数组进行升序排序`）
  - 对于多重建议，可悬停查看补全面板（Ctrl+Enter）浏览所有选项

### 3.2 Copilot 对话

通过自然语言与 Copilot 交互，实现提问、生成代码或调试功能

- **开启对话**：
  - 从活动栏打开**对话视图**，或使用 **Ctrl+Alt+I**（Windows/Linux）/**Cmd+Ctrl+I**（macOS）
  - 也可通过**行内对话**（Ctrl+I 或 Cmd+I）在编辑器中直接进行上下文查询
- **应用场景**：
  - **解释代码**：选择代码块，开启行内对话，输入 `explain this code`
  - **生成代码**：在对话视图中输入 `write a Python function to reverse a string`
  - **调试**：将错误信息粘贴至对话窗口请求修复
- **示例**：
  在对话视图中输入：

  ```
  什么是递归？
  ```

  Copilot 将返回包含 Markdown 代码示例的详细解释

- **斜杠命令**：
  使用 `/explain`、`/doc`、`/fix`、`/tests` 或 `/optimize` 等指令指定任务。例如：

  ```
  /explain this function
  ```

  配合选中的函数可生成详细解析

### 3.3 代理模式（预览版）

代理模式支持 Copilot 自主处理多步骤编码任务，如创建应用、重构代码或编写测试

- **使用方法**：
  - 在 VS Code Insiders 或稳定版中打开 **Copilot 编辑视图**
  - 从模式下拉菜单选择**代理**
  - 输入提示词，例如 `创建包含姓名和邮箱字段的 React 表单组件`
  - Copilot 将分析代码库，建议修改，并可运行终端命令或测试
- **能力范围**：
  - 跨多文件生成代码
  - 监控错误并迭代修复问题
  - 集成新库或将代码迁移至现代框架

> **注意**：代理模式尚处实验阶段，在小型代码库中表现最佳。可通过 VS Code GitHub 代码库提交反馈。[](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode)

### 3.4 自定义指令

根据编码风格或项目需求定制 Copilot 行为

- **设置方法**：
  - 在工作区创建 `.github/copilot-instructions.md` 文件
  - 添加 Markdown 格式的指令，例如 `Python 变量名使用蛇形命名法`
  - 在**设置** > **GitHub** > **Copilot** > **启用自定义指令**中激活（需 VS Code 17.12 或更高版本）
- **示例**：

  ```markdown
  # Copilot 自定义指令
  - JavaScript 变量使用驼峰命名法
  - 异步操作优先使用 async/await 而非 .then()
  ```

  Copilot 将根据这些偏好调整建议

### 3.5 工作区上下文查询 @workspace

通过 `@workspace` 命令查询整个代码库

- **示例**：
  在对话视图中输入：

  ```
  @workspace 数据库连接字符串在何处配置？
  ```

  Copilot 将搜索工作区并引用相关文件

### 3.6 下一编辑建议（预览版）

Copilot 根据近期变更预测并推荐后续逻辑编辑

- **运行机制**：
  - 编辑代码时，Copilot 会高亮潜在后续编辑
  - 通过 **Tab** 接受建议，或通过行内对话修改
- **应用场景**：适用于迭代重构或完成关联代码修改

## 4. Copilot 优化使用技巧

### 4.1 编写高效提示词

- 具体明确：用 `编写按'age'键对字典列表排序的 Python 函数` 替代 `编写函数`
- 提供上下文：包含框架或库细节（例如 `使用 React hooks`）
- 善用注释：通过 `// 用 Express 生成 REST API 端点` 引导补全

### 4.2 活用上下文

- **引用文件/符号**：在对话提示中使用 `#文件名`、`#文件夹` 或 `#符号` 限定上下文范围

  ```
  /explain #src/utils.js
  ```

- **拖拽操作**：将文件或编辑器标签页拖入对话提示框添加上下文
- **附加图片**：在 VS Code 17.14 Preview 1 及以上版本中，可附加截图说明问题（如 UI 缺陷）

### 4.3 使用斜杠命令

- `/doc`：为函数生成文档
- `/fix`：针对错误提供修复建议
- `/tests`：为选定代码创建单元测试
- 示例：

  ```
  /tests 为此函数生成 Jest 测试
  ```

### 4.4 保存与复用提示词

- 在 `.github/prompts/` 目录创建 `.prompt.md` 文件存储可复用提示词
- 示例：

  ```markdown
  # React 组件提示词
  生成使用 Tailwind CSS 样式的 React 函数组件。若未提供组件名和属性，请主动询问
  ```

- 在对话中附加提示词实现跨项目复用

### 4.5 选择合适的模型

- Copilot 支持多语言模型（如 GPT-4o、Claude Sonnet）
- 在对话视图下拉菜单中选择模型以适应快速编码或深度推理需求
- 复杂任务中，Claude Sonnet 在代理模式下可能表现更佳。[](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode)

### 4.6 建立工作区索引

- 启用工作区索引以加速代码搜索精度
- 对 GitHub 代码库使用远程索引，大型代码库使用本地索引

## 5. 最佳实践

- **审查建议**：始终验证 Copilot 建议的准确性和项目规范符合度
- **结合 IntelliCode**：在 Visual Studio 中，Copilot 可与 IntelliCode 互补增强补全效果。[](https://devblogs.microsoft.com/visualstudio/github-copilot-in-visual-studio-2022/)
- **安全检查**：Copilot 可能推荐含漏洞的代码。敏感项目中需严格审查建议，并遵循组织策略。[](https://medium.com/%40codebob75/how-to-use-copilot-in-visual-studio-a-step-by-step-guide-b2a5db3b54ba)
- **使用有意义命名**：描述性变量和函数名可提升建议质量
- **对话迭代**：若初始建议不理想，可优化提示词重复尝试
- **监控使用限额**：免费版用户需通过 GitHub 账户设置或 VS Code 的 Copilot 徽章跟踪月度使用量。[](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-free-plan?view=vs-2022)

## 6. 常见问题排查

- **Copilot 未激活**：确认已使用具备 Copilot 权限的 GitHub 账户登录，通过状态栏下拉菜单刷新凭证
- **无建议提示**：检查网络连接或切换至支持的语言，在**工具** > **选项** > **GitHub Copilot** 中调整设置
- **功能受限**：达到免费版使用限额后将切换至 IntelliCode 建议，可升级付费方案或查看使用状态。[](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-free-plan?view=vs-2022)
- **网络问题**：参阅 [GitHub Copilot 故障排除指南](https://docs.github.com/en/copilot/troubleshooting)

## 7. 高级应用场景

- **数据库查询**：要求 Copilot 生成 SQL 查询（例如 `编写连接两表的 SQL 查询`）
- **API 开发**：请求生成 API 端点代码（例如 `创建处理 POST 请求的 Flask 路由`）
- **单元测试**：使用 `/tests` 为 Jest 或 Pytest 等框架生成测试
- **代码重构**：通过代理模式跨文件重构代码（例如 `将 jQuery 代码迁移至 React`）

## 8. 隐私与安全考量

- **数据使用**：Copilot 会实时传输代码片段至 GitHub 服务器生成建议，但不会保留数据（企业版立即丢弃片段）。[](https://medium.com/%40codebob75/how-to-use-copilot-in-visual-studio-a-step-by-step-guide-b2a5db3b54ba)
- **公共代码匹配**：Copilot 可能推荐与公共 GitHub 代码库匹配的代码，可启用代码引用查看许可证详情。[](https://learn.microsoft.com/en-us/visualstudio/ide/visual-studio-github-copilot-extension?view=vs-2022)
- **组织策略**：部分组织可能禁用对话或限制建议，使用前请确认合规性。[](https://docs.github.com/en/copilot/quickstart)
- **遥测数据**：如需可在 VS Code 设置中关闭遥测功能。[](https://code.visualstudio.com/docs/copilot/setup)

## 9. 扩展学习资源

- [GitHub Copilot 官方文档](https://docs.github.com/en/copilot)
- [VS Code Copilot 快速入门](https://code.visualstudio.com/docs/copilot/copilot-quickstart)
- [Copilot 对话教程](https://code.visualstudio.com/docs/copilot/copilot-chat)
- [VS Code Copilot 系列视频](https://www.youtube.com/playlist?list=PLj6YeMhvp2S6X0vF4TrRkpZ7GIqM3oPWp)
- [GitHub Copilot 常见问题解答](https://docs.github.com/en/copilot/faq)

## 10. 结语

GitHub Copilot 作为 VS Code 中的强力工具，通过智能建议、问题解答和复杂任务自动化显著提升编码效率。正确配置设置、灵活运用功能特性并遵循最佳实践，将助您聚焦创造性编程任务。建议积极尝试 Copilot 的各项能力，根据工作流进行定制化调整，同时保持对安全性和使用限额的关注，充分发挥这位 AI 编程伙伴的潜能。
