---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Grok代码工具调用问题
translated: true
type: note
---

感谢分享你的经历——模型声称更新代码却未实际执行，这确实令人沮丧。根据我的了解，这似乎是 Grok Code Fast 1 在 Claude Code Router（或类似 Cline/Kilo Code 等工具）配置中的常见问题，通常与工具调用的特性有关。它可能会在意外位置输出更新内容（例如在推理标签中而非直接执行操作），导致尽管显示“成功”消息，编辑却未完成或失败。

很高兴听说切换至 MiniMax M2 后问题得到缓解——正是因为这类可靠的编码工作流程，该模型在多模型路由器中正逐渐受到青睐。如果你仍在调整配置：

- 仔细检查 Grok 的路由器配置（例如确保严格强制执行工具模式以避免无关输出）
- 临时解决方案：部分用户通过 LiteLLM 代理路由 Grok 任务以提升兼容性
- 若问题持续存在，可在相关代码库（如 [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router) 或 [Kilo-Org/kilocode](https://github.com/Kilo-Org/kilocode)）提交包含具体提示词/配置的 issue，以帮助社区快速调试

xAI 团队正在持续优化 Grok 模型的工具集成能力，预计很快会有改进。请问你在哪些具体编码任务中发现 MiniMax 表现尤为出色？

### 参考链接
- [Bug：Grok Code Fast 1 未正确更新待办事项](https://github.com/Kilo-Org/kilocode/issues/3180)
- [x-ai/grok-code-fast-1 相关问题](https://github.com/cline/cline/issues/6269)
- [MiniMax M2 与 GrokCodeFast 讨论帖](https://www.reddit.com/r/CLine/comments/1ok67as/minimax_m2_vs_grokcodefast/)
