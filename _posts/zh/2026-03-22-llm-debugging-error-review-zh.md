---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM 调试：错误日志和审查
translated: true
type: note
---

问题：在使用 LLM 进行调试时，复制浏览器 console logs 或 HTTP 请求错误是否特别有效？虽然有些人说你不需要阅读 AI 生成的代码，但快速审查它不是有助于获得更好帮助的额外优势吗？

回答：

## 使用 LLM 进行调试：Console Logs、HTTP Errors 和代码审查

### 为什么 Console Logs 和 HTTP Errors 对 LLM 是黄金信息

是的——粘贴原始的浏览器 console 输出或 network errors 是从 LLM 获取有用帮助的 **最有效方式之一**，原因如下：

**1. Errors 已经是结构化信息**
- Stack traces、error codes 和 HTTP status messages 精确且明确
- LLM 在 Stack Overflow、GitHub issues、MDN 等海量类似 error patterns 上训练
- 没有“翻译损失”——你直接给出运行时产生的精确内容

**2. HTTP errors 特别具有诊断性**
- `401 Unauthorized` 与 `403 Forbidden` 或 `CORS error` 各自讲述完全不同的故事
- Network tab 细节（request headers、response body、URL、method）为 LLM 提供完整上下文以精确定位根本原因
- AI 可以立即区分“你的 token 错误”与“你的服务器不允许跨域请求”

**3. Console logs 消除歧义**
- 与你 *描述* bug（“它不工作”）不同，log *显示* bug
- Null reference errors、type mismatches、undefined variables——在 log 中一目了然

---

### “你不需要阅读 AI 代码”的争论

有些人认为你可以盲目运行 AI 生成的代码。对于简单脚本，这部分正确——但 **快速审查确实有价值**，原因如下：

| 场景 | 跳过审查 | 快速审查 |
|---|---|---|
| 简单的 5 行实用工具 | ✅ 可以 | ✅ 也可以 |
| 涉及 auth/security 的代码 | ❌ 风险高 | ✅ 必需 |
| 修改 database/files 的代码 | ❌ 风险高 | ✅ 必需 |
| 大型多函数输出 | ❌ 后续调试困难 | ✅ 及早发现不匹配 |
| 你需要后续维护它 | ❌ 你会迷失 | ✅ 你会理解它 |

**即使 30 秒快速浏览也能帮助你：**
- 发现 AI 是否误解了你的意图
- 注意硬编码的值应该改为变量
- 在运行前捕获明显的逻辑错误
- 提供更好的后续反馈（“你用了 POST 但我需要 GET”）

---

### 反馈循环：真正的力量

真正的协同效应是 **循环**：

```
你粘贴 error → AI 解释并修复 → 你快速浏览修复
→ 你运行它 → 出现新 error → 你粘贴该 error
→ AI 因为上下文积累而更快缩小范围
```

每次粘贴真实 error 都能 **将对话 grounding 在现实中** 而非猜测。AI 不是猜测可能的问题——它在阅读 *实际* 的问题。

---

### 实用提示

- **粘贴完整的 error**，而非摘要——行号和 stack frames 等细节很重要
- **连同 error 一起包含相关代码块** 以实现更快诊断
- API 问题时 **Network tab > Console**——复制完整的 request/response
- 快速扫描 AI 代码是一种 **低成本、高回报的习惯**——即使 20 秒审查也值得
