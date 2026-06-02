---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 快速获取更好的 Zoom 会议总结
translated: true
type: note
---

你说得对 —— Zoom AI Companion 存在输出限制，这使得处理长时间会议变得具有挑战性。以下是一些更好的策略：

## Workaround Strategies

### **Strategy 1: Use Zoom's Meeting Summary Feature**

会议结束后：
- Zoom AI Companion 会自动生成完整的 meeting summary
- 通过 Zoom Web Portal，在 "Meetings" → "Recorded" 标签页下访问它
- 下载 summary 和 transcript
- 然后向 AI Companion 提问或使用 ChatGPT/Claude：“将这段 transcript 分成 5 分钟一段的段落，且不包含参与者姓名”

### **Strategy 2: Incremental Extraction During Meeting**

会议期间，每隔 5 分钟逐步提问：
- "Summarize minutes 0-5 without names"
- "Summarize minutes 5-10 without names"
- "Summarize minutes 10-15 without names"

立即将每个回复复制到你的文档中。

### **Strategy 3: Use Recording + Post-Processing (Best Option)**

1. **Record the meeting**（需征得参与者同意）
2. **会议结束后**，从 Zoom 下载 transcript
3. **上传 transcript** 至：
   - ChatGPT（付费版本可以处理长文本 transcript）
   - Claude（可以处理超长文档）
   - Google Gemini
4. **提问**：“将这一小时长的 transcript 分成 5 分钟一段的段落，总结每个段落的关键点，并移除所有参与者姓名”

### **Strategy 4: Third-Party Tools**

考虑与 Zoom 集成的第三方工具：
- **Otter.ai** - 带有 timestamps 的实时 transcription
- **Fathom** - AI meeting notes
- **Fireflies.ai** - 分段录制并汇总

这些工具通常比 Zoom 原生的 AI Companion 具有更好的分段功能。

**哪种方法最适合你的 workflow？** 对于长达一小时的会议，recording + post-processing 方法通常能提供最全面的结果。
