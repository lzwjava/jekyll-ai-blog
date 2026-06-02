---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最佳转录文本整理模型指南
translated: true
type: note
---

绝佳应用场景。针对**需要严格格式且“杜绝冗余内容”的长文本转录整理**，以下是在OpenRouter上目前各场景下的最佳选择。

**快速+经济型主力（中英文/长文件）：DeepSeek-V3.1**
指令遵循能力强，支持128k上下文，可根据文本混乱程度切换“思考模式”。在中英文填充词删除和统一说话人标签方面表现优异。（[DeepSeek API文档][1]、[OpenRouter][2]）

**中文访谈与口语化内容：Kimi K2 Instruct**
月之暗面的K2（混合专家）模型对中文俚语和风格处理尤为流畅，适合以中文为主的转录稿且能保留技术术语。（[OpenRouter][3]）

**编辑指令遵循度最高：Claude Sonnet (3.7/4)**
Anthropic的Sonnet系列擅长“仅输出精炼文本，不附加说明”，对语义修改保持谨慎，特别适合需要严格遵循操作步骤的场景。优先选用Sonnet 4，3.7版本同样出色。（[OpenRouter][4]）

**超长会话或单次全局处理：GPT-5**
当需要处理超大上下文且保持低幻觉率时，GPT-5是OpenRouter前沿模型中最稳妥的选择（标注支持超大上下文，具备强大的推理和编辑能力）。适用于马拉松式转录稿或最终润色环节。（[OpenRouter][5]）

**同样强劲但需关注成本：Gemini 2.5 Pro**
在推理和长文本编辑方面表现突出。虽然精修效果可靠，但需根据供应商路线留意定价/配额。（[OpenRouter][6]）

---

### 实用调度方案（无表格版）

* **≤128k token，中英文混合，注重速度**：DeepSeek-V3.1（非思考模式）。仅当段落混乱时开启思考模式。（[DeepSeek API文档][1]）
* **中文为主转录稿**：Kimi K2 Instruct。（[OpenRouter][3]）
* **严格“编辑”模式（无注释），法律/金融语体**：Claude Sonnet。（[OpenRouter][4]）
* **巨型文件或最终单次润色**：GPT-5。（[OpenRouter][5]）

---

### 增强稳定性的代码调整

* **支持模型选择**：添加`--model`命令行参数，默认设为`deepseek-v3.1`
* **自动按规模/语言路由**：检测token数量和中文比例，中文密集型任务选用K2，超大输入选用GPT-5，严格编辑模式选用Claude
* **思考模式开关**（DeepSeek）：在调用OpenRouter时添加参数设置`reasoning.enabled`以处理复杂段落（[DeepSeek API文档][1]）
* **修复细节问题**：修正游离的`print(".1f")`语句；扩展说话人标签正则表达式以支持`A：`（全角冒号）及无空格变体
* **防护机制**：当长度差异>10%时自动重试并提示“勿删除内容”；未检测到`A:`/`B:`标签时自动重试并提示“标注说话人”

如需立即实现，我可以为您重写脚本，加入`--model`参数和智能路由逻辑。

[1]: https://api-docs.deepseek.com/quick_start/pricing?utm_source=chatgpt.com "模型与定价"
[2]: https://openrouter.ai/deepseek/deepseek-chat-v3.1?utm_source=chatgpt.com "DeepSeek V3.1 - API、供应商、数据"
[3]: https://openrouter.ai/moonshotai/kimi-k2?utm_source=chatgpt.com "Kimi K2 - API、供应商、数据"
[4]: https://openrouter.ai/anthropic/claude-3.7-sonnet?utm_source=chatgpt.com "Claude 3.7 Sonnet - API、供应商、数据"
[5]: https://openrouter.ai/openai/gpt-5?utm_source=chatgpt.com "GPT-5 - API、供应商、数据"
[6]: https://openrouter.ai/google/gemini-2.5-pro?utm_source=chatgpt.com "Gemini 2.5 Pro - API、供应商、数据"
