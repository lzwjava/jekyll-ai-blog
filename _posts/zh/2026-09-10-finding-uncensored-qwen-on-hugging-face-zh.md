---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Hugging Face上寻找未审查的Qwen
translated: true
type: note
---

问题：**如何在Hugging Face上找到像Qwen变体这样的无审查模型？**

答案：最简单的方法是使用Hugging Face的**`uncensored`过滤器/搜索**，然后检查模型卡片，而不是仅凭名称判断。

### 1. 直接使用Hugging Face搜索

[Hugging Face — 无审查模型](https://huggingface.co/models?other=uncensored&utm_source=chatgpt.com)

目前会显示以下模型：

* `OBLITERATUS/Qwen3.8-27B-OBLITERATED`
* `huihui-ai/Huihui-Qwen3.8-27B-abliterated`
* `orcarouter/Qwen3.8-27B-Uncensored-GGUF`
* `JonathanColetti/Qwen3.8-27B-Uncensored-GGUF`
* `DavidAU/Qwen3.8-27B-TURBO-...-Heretic-Uncensored...`

([Hugging Face][1])

### 2. 实际有效的搜索词

在HF上，尝试以下组合：

```text
qwen uncensored
qwen abliterated
qwen heretic
qwen obliterated
qwen uncensored gguf
qwen uncensored 4bit
qwen uncensored 8b
qwen uncensored 14b
qwen uncensored 32b
```

关键关键词是：

```text
uncensored
abliterated
obliterated
heretic
unfiltered
```

例如：

[搜索 Qwen3 + uncensored](https://huggingface.co/models?search=qwen3+uncensored&utm_source=chatgpt.com)

HF目前根据查询条件返回数百/数千个变体。([Hugging Face][2])

### 3. 理解术语

人们所说的“无审查”实际上包含几种不同情况：

**A. 微调无审查**

```text
基础 Qwen
    ↓
无审查指令微调
    ↓
模型
```

模型经过训练，拒绝回答的倾向更低。

**B. Abliteration**

```text
Qwen
 ↓
识别拒绝/安全方向
 ↓
修改权重
 ↓
abliterated Qwen
```

这在HF上极为常见。`Huihui-Qwen...-abliterated`、`Heretic`和`OBLITERATED`都是例子。([Hugging Face][3])

**C. 合并**

例如：

```text
Qwen
 + 另一个微调模型
 + 另一个模型
 + 去除拒绝机制模型
 = 合并模型
```

这便是模型名称变得离谱的原因：

```text
Qwen3.8-27B
  → Fable
  → Cold Fusion
  → Heretic
  → Uncensored
  → NEO
  → CODER
  → MTP
```

你之前提到的 `DavidAU/...TURBO-Fable-Cold-Fusion...` 正是这类社区模型。([Hugging Face][2])

### 4. 根据硬件筛选

对于你自己的机器而言，这比单纯搜索 `uncensored` 更有用。

例如，使用 **12 GB 4070**，搜索：

```text
qwen uncensored 4bit
qwen abliterated GGUF
qwen 8B uncensored
qwen 9B uncensored
```

然后选择：

```text
4B / 8B / 9B
↓
Q4_K_M / Q4_K_S / IQ4
↓
GGUF
```

例如，HF目前有 `Qwen3.5-9B` 和 `Qwen3.5-4B` 的无审查变体，以及许多27B版本。([Hugging Face][4])

对于 **27B**，你仍然可以运行量化版本，但VRAM/内存和速度会成为限制。

### 5. 我偏好的HF工作流

与其搜索：

```text
"best uncensored model"
```

我会这样做：

```bash
# 从命令行/浏览器搜索HF
huggingface-cli search qwen uncensored
```

或者直接使用HF搜索URL，然后筛选：

```text
模型名称：       qwen3
任务：           文本生成
库：             GGUF
参数量：         4B–14B
排序：           下载量 / 趋势
```

然后检查：

```text
README
文件
量化
基础模型
许可证
下载量
点赞数
近期更新
```

**不要仅凭文件名中的“UNCENSORED”就信以为真。** 某些社区模型经过了大量合并/量化，其行为可能与原始模型有显著差异。

具体到你的情况，我建议从 **Qwen3/Qwen3.5/Qwen3.8 8–9B 无审查/abliterated GGUF** 开始，在本地进行基准测试，如果行为值得额外计算资源，再升级到27B。([Hugging Face][4])

参考资料：

* [Hugging Face Models — uncensored filter](https://huggingface.co/models?other=uncensored&utm_source=chatgpt.com)
* [Hugging Face Models — Qwen3 uncensored search](https://huggingface.co/models?search=qwen3+uncensored&utm_source=chatgpt.com)
* [Hugging Face Models](https://huggingface.co/models?utm_source=chatgpt.com)

[1]: https://huggingface.co/models?other=uncensored&utm_source=chatgpt.com "Models – Hugging Face"
[2]: https://huggingface.co/models?search=qwen+uncensored&utm_source=chatgpt.com "Models – Hugging Face"
[3]: https://huggingface.co/models?other=qwen3&utm_source=chatgpt.com "Models – Hugging Face"
[4]: https://huggingface.co/models?search=qwen3+4b+uncensored&utm_source=chatgpt.com "Models – Hugging Face"