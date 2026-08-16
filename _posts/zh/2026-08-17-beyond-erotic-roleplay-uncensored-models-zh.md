---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 超越情色角色扮演：无审查模型
translated: true
type: note
---

问题：**人们实际上用“未经审查”/“无审查”的模型来做什么？主要用于生成色情故事吗？**

回答：**是的，情色/NSFW角色扮演和虚构故事是一个主要用例，但绝对不是唯一的。**

有趣的是，“未经审查”实际上是指**移除或弱化模型的拒绝/对齐行为**，而不是一个能力类别。社区模型通过微调、模型合并或*abliteration*（移除拒绝方向）等方式实现这一点。（[GetLLMs][1]）

典型用例：

| 用例                               | 人们想要未经审查模型的原因                                                     |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| **情色小说 / 角色扮演**            | 托管模型常常拒绝；本地模型则不会                                                 |
| **角色扮演**                       | 在黑暗、暴力、有争议或异常角色上拥有更多自由                                     |
| **黑暗小说 / 恐怖**                | 不受安全拒绝的中断减少                                                           |
| **创意写作**                       | 对主题和角色的限制更少                                                           |
| **隐私**                           | 敏感对话停留在你的机器上                                                         |
| **红队测试 / 对齐研究**            | 研究当拒绝行为被移除时会发生什么                                                   |
| **编程 / 技术工作**                | 避免在安全、系统或争议性技术主题上出现误报拒绝                                     |
| **模型实验**                       | 比较基础模型 → 指令微调 → 对齐 → 消融后的行为                                    |
| **自定义助手**                     | 用你自己的策略而非提供商的策略构建一个助手                                           |

一项 2026 年对开源模型用户的研究明确指出，**恐怖写作和情色角色扮演**是未经审查微调模型的使用场景之一。（[ResearchGate][2]）

### 色情/ERP 的部分是真实的

围绕它有一个完整的生态系统：

```text
未经审查的 LLM
      │
      ├── 角色卡
      ├── 长期记忆
      ├── lorebooks（背景故事库）
      ├── 角色扮演前端
      │
      └── 本地推理
             │
             ├── llama.cpp
             ├── Ollama
             └── vLLM
```

人们将未经审查的模型与角色扮演前端以及角色/人格系统结合使用。甚至有一些模型集合被明确归类为**“创意写作和角色扮演”**以及**ERP**。（[RunThisModel][3]）

但我不会将整个生态系统描述为“色情模型”。

从技术角度更有趣的动机是：

> **“我拥有模型，我来决定策略。”**

这对于本地 AI 尤其有吸引力。你的模型不会因为托管提供商更改了审核策略而突然改变行为，私人对话也不需要经过别人的服务器。本地 AI 社区明确将隐私、定制化和控制权作为使用这些模型的原因。（[Reddit][4]）

对于像你这样正在尝试训练的人来说，**abliteration 实际上是一个相当值得研究的现象**：

```text
基础模型
    ↓
指令微调
    ↓
RLHF / 偏好优化
    ↓
拒绝行为出现
    ↓
消融 / 微调
    ↓
拒绝行为减少
```

然后你可以测量：

```text
能力
   vs
拒绝率
   vs
对齐程度
   vs
模型质量
```

从 LLM 工程的角度来看，这比单纯的“生成色情内容”有趣得多。

### 一个重要区别

“未经审查”≠“更智能”。

例如，一些社区模型实际上是**未经指令/对齐训练的基础模型**，而另一些则是经过大幅修改的指令微调模型。有些模型惊人地保留了能力；另一些则在推理或指令遵循方面变得更差。（[Hugging Face][5]）

所以，如果你以 LLM 工程师的视角来看，我建议把这个生态系统看作一场自然实验，其主题是：

**预训练 → SFT → 偏好优化 → 拒绝回路 → 行为修改。**

这才是真正有趣的部分。

参考文献：

* [Open AI in the Wild: Adoption and Adaptation of Open Models](https://www.researchgate.net/publication/407506999_Open_AI_in_the_Wild_Adoption_and_Adaptation_of_Open_Models_on_rLocalLLaMA?utm_source=chatgpt.com)
* [Hugging Face — Llama-3-8B-Lexi-Uncensored](https://huggingface.co/Andycurrent/Llama-3-8B-Lexi-Uncensored?utm_source=chatgpt.com)
* [Uncensored Local AI Models](https://runthismodel.com/uncensored?utm_source=chatgpt.com)
* [LocalLLaMA discussion on uncensored models](https://www.reddit.com/r/LocalLLaMA/comments/1qsvgsh/some_uncensored_models/?utm_source=chatgpt.com)

[1]: https://getllms.org/concepts/uncensored-model?utm_source=chatgpt.com "Uncensored Model: Definition, Sources, FAQs and Related Pages | GetLLMs"
[2]: https://www.researchgate.net/publication/407506999_Open_AI_in_the_Wild_Adoption_and_Adaptation_of_Open_Models_on_rLocalLLaMA?utm_source=chatgpt.com "(PDF) Open AI in the Wild: Adoption and Adaptation of Open Models on r/LocalLLaMA"
[3]: https://runthismodel.com/uncensored?utm_source=chatgpt.com "Uncensored Local AI Models — Hardware-Filtered | RunThisModel · RunThisModel"
[4]: https://www.reddit.com/r/LocalLLaMA/comments/1r5ki6g/building_a_fully_local_ai_roleplay_app_private/?utm_source=chatgpt.com "Building a fully local AI roleplay app (private, customizable, experimental) — would this interest you?"
[5]: https://huggingface.co/helmies/helmies-uncensored?utm_source=chatgpt.com "helmies/helmies-uncensored · Hugging Face"
