---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 快速升级Claude代码
translated: true
type: note
---

如果你想**升级Claude Code**——Anthropic公司推出的命令行编程助手，以下是具体操作步骤，让你能顺利使用最新功能，包括学习模式与自定义子代理。

---

### 如何升级Claude Code

1. **检查当前版本**
   运行命令：

   ```
   claude --version
   ```

   即可查看当前安装的版本号。

2. **通过npm更新**
   最简单的升级方式：

   ```
   npm install -g @anthropic-ai/claude-code@latest
   ```

   该命令会从npm拉取最新版本。
   海外用户反馈此操作修复了卡顿问题并提升了响应速度。有人写道：

   > “更新到最新版（1.0.18）后体验天差地别——代码生成更智能，响应更迅捷。”
   > ([Reddit][1], [Anthropic][2])

3. **使用原生安装包（Beta版）**
   若倾向独立二进制文件（非npm依赖），可尝试：

   ```
   curl -fsSL https://claude.ai/install.sh | bash -s latest
   ```

   （Windows系统请使用PowerShell版本）
   ([Anthropic][3])

4. **验证更新结果**
   安装完成后重启终端，再次运行 `claude --version` 确认新版本已激活。

5. **安装问题排查**
   若遇安装障碍，可先卸载旧版：

   ```
   npm uninstall -g @anthropic-ai/claude-code
   npm install -g @anthropic-ai/claude-code
   ```

   部分用户通过此操作解决了更新异常。([Anthropic][4], [Reddit][1], [Anthropic][5], [The Verge][6])

---

### 新版特性详解

#### 学习模式

Anthropic近期为Claude Code新增**解说模式**与**学习模式**，不仅能生成代码，更会阐释背后的逻辑推理。启用方法：

1. 确保Claude Code已更新至最新版
2. 在Claude Code会话中运行 `/output-styles`
3. 选择**默认**、**解说**或**学习**模式
   该功能于**2025年8月14日**正式发布。([Tom's Guide][7])

#### 自定义子代理

Claude Code现支持**子代理**——专用于特定场景的AI助手（如修复漏洞、代码重构、文档撰写）。每个子代理可独立设置系统指令、工具权限与上下文长度。
创建步骤：

1. 运行 `/agents`
2. 选择“创建新代理”（支持用户级或项目级）
3. 定义其行为模式、可用工具并保存
   子代理能有效优化工作流，保持任务专注度与场景感知力。([Anthropic][8])

---

### 要点速览（无表格，清晰步骤）

* **升级方式**：

  ```
  npm install -g @anthropic-ai/claude-code@latest
  ```

  或使用原生安装命令 `curl | bash -s latest`

* **启用学习模式**：
  * 完成升级
  * 在Claude Code中运行 `/output-styles` 选择模式

* **创建子代理**：
  * 在Claude Code中运行 `/agents`
  * 自定义工具权限、系统指令与行为模式

---

### 总结

升级Claude Code流程简明——通过npm或原生安装器更新至最新版，即可体验**学习模式**与**子代理**功能。这些新特性正将Claude Code从单纯的编程助手，转型为开发流程中的教学伙伴与智能协作体。

若需指导创建首个子代理或高效使用学习模式，我随时为您提供详细指引！

[1]: https://www.reddit.com/r/ClaudeAI/comments/1l8gbfo/dont_forget_to_update_your_claude_cli_it_makes_a/?utm_source=chatgpt.com "别忘了更新Claude命令行工具！效果大不同..."
[2]: https://www.anthropic.com/solutions/agents?utm_source=chatgpt.com "Claude智能代理 | Anthropic人工智能解决方案"
[3]: https://docs.anthropic.com/en/docs/claude-code/quickstart?utm_source=chatgpt.com "快速入门 - Claude Code"
[4]: https://docs.anthropic.com/en/docs/claude-code/settings?utm_source=chatgpt.com "Claude Code设置"
[5]: https://docs.anthropic.com/en/docs/claude-code/overview?utm_source=chatgpt.com "Claude Code概览"
[6]: https://www.theverge.com/2024/11/25/24305774/anthropic-model-context-protocol-data-sources?utm_source=chatgpt.com "Anthropic推出连接AI系统与数据集的新工具"
[7]: https://www.tomsguide.com/ai/claudes-new-learning-modes-take-on-chatgpts-study-mode-heres-what-they-do?utm_source=chatgpt.com "Claude新推「学习模式」对标ChatGPT学习模式——功能详解"
[8]: https://docs.anthropic.com/en/docs/claude-code/sub-agents?utm_source=chatgpt.com "子代理系统"
