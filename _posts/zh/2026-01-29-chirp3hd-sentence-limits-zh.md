---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Chirp 3 HD 句子长度限制详解
translated: true
type: note
---

**Chirp 3 HD voices**（Google Cloud Text-to-Speech 中 Chirp 3 的高级版本）与 WaveNet 等旧模型相比，对 **maximum sentence length** 有更严格的内部限制。这会导致以下错误：

> 400 This request contains sentences that are too long. Consider splitting up long sentences with sentence ending punctuation e.g. periods.

这 **不是** 整体请求字符限制（大多数 voices 的同步请求通常为 ~5000 characters/bytes）。相反，这是模型特定的约束，限制单个句子（标点符号如句号、问号等之间的文本）在模型拒绝处理或产生 artifacts/errors 之前的最大长度。

### Key Limits Comparison

- **Overall request size (synchronous synthesizeSpeech)**  
  大多数 voices，包括 Chirp 3 HD 和 WaveNet，为 ~5000 characters（包括空格，SSML tags 也计入）。  
  超过此限制会产生不同的错误（例如 quota exceeded 或 payload too large）。

- **Per-sentence length limit**  
  - Chirp 3 HD（以及许多 Neural2 / 新型 neural voices）：似乎强制执行更低的每个句子阈值——通常在句子超过大约 **200–500 characters** 时失败（确切阈值因语言、voice 和内容复杂度而异）。  
    这在日语、中文等语言，或句子包含长数字、列表或 run-on structures 时尤为明显。  
    解决方法：  
    - 使用句号、问号或感叹号拆分长句子。  
    - 添加换行或额外标点。  
    - 将输入拆分为多个较短请求并拼接音频。

  - WaveNet（较旧的 premium voices）：**不** 强制执行此严格的每个句子限制（或执行更高的限制）。  
    它通常可以处理更长的单个句子，而不会出现“sentences too long”错误，这就是为什么只在 Chirp 3 HD 中出现此问题，而 WaveNet 没有。

- **Long-form synthesis** (asynchronous, via Long Audio Synthesis)  
  总输入高达 ~1 million characters（存储在 GCS 中）。  
  然而，用户报告显示 Chirp 3 HD 有时会在中等长输入（例如 15k characters）上卡住或失败，而 standard/WaveNet voices 可以成功完成。

### Why the Difference?

- Chirp 3 HD 是一种更先进的生成模型，针对 naturalness、expressiveness 和低延迟进行了优化（特别是在 streaming/real-time 用例如 Gemini Live 中）。  
- 这些模型对输入结构更敏感——没有中断的超长句子可能导致 prosody 差、不稳定生成或内部处理失败（例如 attention mechanisms 或 transformer context limits）。  
- 为了维持高质量并避免坏输出，Google 在 Chirp 3 HD 中添加了硬检查，拒绝过长的句子。  
- WaveNet（较旧的 concatenative/neural 架构）对长输入更宽容，但许多情况下听起来不太自然。

### Practical Advice (as of early 2026)

- 对于 Chirp 3 HD：尽可能将单个句子保持在 ~300–400 characters 以内。积极使用标点创建自然停顿。  
- 如果需要非常长的连续文本 → 回退到 WaveNet voices（如果在您的 locale 中仍可用）或拆分 synthesis 请求。  
- 对于非常长的内容 → 使用 long-form async API，但需彻底测试 Chirp 3 HD，因为并非所有 voices/inputs 都能保证稳定性。  
- Chirp 3 HD 的 SSML 支持有限（标签子集），因此无法像旧模型那样始终使用 `<s>` 或 `<p>` 强制中断。

References:  

- https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd
- https://discuss.google.dev/t/this-request-contains-sentences-that-are-too-long-consider-splitting-up-long-sentences/130332
- https://calvincchan.com/blog/250531-google-tts-with-chirp3-hd-in-japanese
- https://discuss.google.dev/t/long-form-audio-does-not-work-with-chirp3-hd-voices/194335
- https://cloud.google.com/text-to-speech/quotas