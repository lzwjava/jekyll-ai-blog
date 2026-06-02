---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI模型成本与性能指南
translated: true
type: note
---

以下是各模型**基准测试分数**和**API定价**的清晰拆解——包括Claude 4 Opus（亦标注为Claude Opus 4）、GPT‑5（标准版/完整版）、GPT‑5 Mini、GPT‑5 Nano，以及o3（OpenAI）和Claude 4 Sonnet——为避免冗杂，此处不使用表格。

---

## 基准测试表现 (SWE-bench)

此项反映模型在软件工程任务上的表现：

* **Claude 4 Opus (2025年5月14日)**: 67.60
* **GPT‑5 (2025年8月7日，中等推理)**: 65.00
* **Claude 4 Sonnet (2025年5月14日)**: 64.93 ([SWE-bench][1])

**小结**：Claude 4 Opus在SWE-bench上略占优势，GPT-5和Claude Sonnet紧随其后。

---

## API定价 (每百万token)

### **Claude 4 Opus**

* 输入: **15美元**
* 输出: **75美元** ([Anthropic][2], [LaoZhang AI][3], [Simon Willison’s Weblog][4])

### **GPT-5 (标准版/完整版)**

* 输入: **1.25美元**
* 缓存输入（重复使用时）: **0.125美元**
* 输出: **10美元** ([OpenAI][5])

### **GPT-5 Mini**

* 输入: **0.25美元**
* 输出: **2美元** ([OpenAI][5], [WIRED][6])

### **GPT-5 Nano**

* 输入: **0.05美元**
* 输出: **0.40美元** ([OpenAI][5], [WIRED][6])

### **o3-mini** (供参考)

* 定价可参考o4‑mini：
* 输入: **1.10美元**，输出: **4.40美元** ([Simon Willison’s Weblog][4])

### **Claude 4 Sonnet**

* 输入: **3美元**，输出: **15美元** ([LaoZhang AI][3])

---

## 核心对比亮点

* **最佳性能**：Claude 4 Opus在编程基准测试中略微领先GPT-5和Claude Sonnet。
* **最低token成本**：

  * **GPT-5 Nano**是目前最经济的选择——非常适合摘要等轻量任务。
  * **GPT-5 Mini**在速度和成本之间取得了平衡。
  * **GPT-5标准版**依然极具成本效益，尤其搭配廉价缓存时优势更明显。
* **Claude系列模型**（Opus和Sonnet）的单token价格显著更高，但其强大的推理和智能体能力足以支撑该定价。

---

## 总结（清晰简明）

* **Claude 4 Opus**：顶级性能，高昂成本（输入15美元/输出75美元）。
* **GPT-5（完整版）**：优异表现（略逊于Opus），成本亲民得多（输入1.25美元/输出10美元）。
* **GPT-5 Mini**：中端预算友好型选择（输入0.25美元/输出2美元）。
* **GPT-5 Nano**：轻量任务或大规模低成本场景的理想选择（输入0.05美元/输出0.40美元）。
* **Claude 4 Sonnet**：成本与性能的折中方案（输入3美元/输出15美元），但基准测试略低于其他模型。

---

如需根据特定使用模式估算**月度成本**，或需要结合提示缓存和批量折扣进行对比，欢迎随时告知！

[1]: https://www.swebench.com/?utm_source=chatgpt.com "SWE-bench排行榜"
[2]: https://www.anthropic.com/pricing?utm_source=chatgpt.com "定价"
[3]: https://blog.laozhang.ai/ai-tools/claude-4-pricing-guide-2025/?utm_source=chatgpt.com "Claude 4.0定价指南：完整成本分析与最佳方案..."
[4]: https://simonwillison.net/2025/Aug/7/gpt-5/?utm_source=chatgpt.com "GPT-5：核心特性、定价与模型卡片"
[5]: https://openai.com/api/pricing/?utm_source=chatgpt.com "API定价"
[6]: https://www.wired.com/story/openais-gpt-5-is-here/?utm_source=chatgpt.com "OpenAI终发布GPT-5，全方位解读在此..."
