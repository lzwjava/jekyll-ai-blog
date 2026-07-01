---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用于自动语音识别的金融音频数据集
translated: true
type: note
---

问题：是否有可用的金融音频数据集用于训练/微调像 Whisper 这样的 ASR 模型？

回答：

有的——金融领域（主要是财报电话会议）实际上是领域专用 ASR 数据覆盖较好的细分方向之一，因为 S&P Global (Kensho) 和学术团队已经发布了大型、自由许可的语料库，专门用于推动 Whisper 类模型的发展。以下是按实际使用价值排序的概览：

**1. SPGISpeech——最适合微调（5000 小时）**
专业转录的财报电话会议，格式完整（包含标点、大小写、ITN 处理），与 Whisper 的归一化输出训练目标一致。SPGISpeech 是一个英语语音识别语料库，由 S&P Global, Inc. 手动转录的公司财报电话会议组成，训练集划分从 200 小时到 5000 小时不等，并包含规范的验证和测试集。

```python
from datasets import load_dataset
spgi = load_dataset("kensho/spgispeech", "s", use_auth_token=True)  # "s"=small/200h, "m", "l"=5000h
```

现在还有一个面向说话人标记/多说话人 ASR 的 v2 扩展：SPGISpeech 2.0 包含额外 3780 小时专业转录的财报电话会议，每个音频片段都包含通话和说话人信息，免费用于非商业用途。

**2. Earnings-21 / Earnings-22——最适合长文本评估，不适合训练**
这些是留作基准测试的集合，不是训练语料库——规模较小，且有意在口音/地区方面保持多样性。
- Earnings-21 是一个 39 小时的语料库，涵盖不同财务板块的公司财报电话会议。
- Earnings-22 包含 125 个文件，总计约 119 小时的英语财报电话会议，来自全球多个国家，涵盖 7 个不同语言区域的说话人，涉及 27 个不同国家，提供完整音频、转录文本以及股票代码、总部国家等元数据。它旨在作为仅测试集——非常适合衡量在口音压力下的词错误率（WER），正是那种长文本/噪声领域场景，Whisper-v3 仍然领先：Whisper-v3 在长金融音频 ASR 上持续实现最低 WER，大约在 12%-16% 范围内，GPT-4o-audio 紧随其后。

```python
earnings22 = load_dataset("distil-whisper/earnings22", split="test")
```

还有一个值得了解的新变体：Contextual Earnings-22 将每个音频片段与现实的定制词汇上下文配对，手动审查和修正转录文本以减少伪影，并针对 STT API（包括 Whisper）评估关键词增强/提示基线。如果你测试的是偏置/上下文词汇技巧（股票代码、高管姓名）而非原始微调，这将很有用。

**3. MAEC——多模态（文本+音频），如果你需要超越 ASR 的对齐能力，这是个好选择**
MAEC 是一个大规模多模态、文本-音频配对的财报电话会议数据集，基于 S&P 1500 公司，规模是此前可用数据集的六倍以上，并特别关注文本-音频对齐过程。如果你的下游目标是从韵律/音频特征预测股票走势而非纯转录，这个数据集更为有用——更接近你对智能体流水线而非原始 ASR 的兴趣。

**4. 非公开：专有工业级规模数据集**
如果你想了解生产环境中流式 Whisper 微调所使用的规模：一篇论文使用了 2023 年之前随机采样的财报电话会议数据作为训练集，得到 5800 小时的音频，转录文本被分割成 5-20 秒的片段，并留出 2023 年之后的 83 个通话（10 小时）作为无泄漏测试集——该论文指出仅 Earnings-22 对于他们的训练需求来说太小了。如果你真的想将 WER 显著降低到低于 SPGISpeech 训练基线的水平，这就是现实的标杆——SPGISpeech 的 5000 小时已经很接近，但你需要结合自己抓取/对齐的财报电话会议音频（Seeking Alpha、Motley Fool 的转录文本 + YouTube/投资者关系音频）才能达到那个规模。

**5. 用于合理性检查的基准**
如果你进行微调，不要仅凭肉眼检查 WER——使用 FinAudio 作为你的评估框架，因为它已经归一化了多个金融 ASR/摘要任务：FINAUDIO 建立了超过 430 小时有组织的金融音频，满足领域特定评估需求，构建了用于短文本 ASR 的 MDRM-test 和 SPGISpeech-test，以及用于长文本 ASR 的 Earnings-21/Earnings-22 测试集，还新增了一个摘要任务。

**针对你的配置（RTX 4070 / MI300X）的实用微调路径：**

```python
# 1. 拉取 SPGISpeech 小规模划分（约 200 小时）——在 4070 上进行 LoRA 微调绰绰有余
from datasets import load_dataset, Audio
ds = load_dataset("kensho/spgispeech", "s", use_auth_token=True)
ds = ds.cast_column("audio", Audio(sampling_rate=16000))

# 2. Whisper 微调框架（标准 HF 配方，根据 4070 显存预算替换为 PEFT/LoRA）
from transformers import WhisperForConditionalGeneration, WhisperProcessor
processor = WhisperProcessor.from_pretrained("openai/whisper-small.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small.en")
# 在 Trainer 之前通过 peft.get_peft_model(...) 应用 LoRA，鉴于你 12GB 显存的限制

# 3. 在 Earnings-22（留出集，真实世界带口音）上评估以获得真实的 WER，而非训练集重叠
eval_ds = load_dataset("distil-whisper/earnings22", split="test")
```

鉴于你可以使用 MI300X（192GB HBM3），对整个 5000 小时的 SPGISpeech "l" 划分进行全量微调（而非 LoRA）实际上可以在一次长时间运行中完成——如果你想做一个与银行领域（金融 NLP/ASR）直接相关、同时又能加强你 AI 原生工具论点的项目，这将比小规模 nanoGPT 工作更有趣。值得在你的 notes-en KB 中记录一下——我注意到那里还没有关于 ASR 微调或 Whisper 内部机制的现有条目；这或许是个不错的开始。

参考文献：

- [FinAudio: A Benchmark for Audio Large Language Models in Financial Applications](https://arxiv.org/html/2503.20990v2)
- [Adapting Whisper for Streaming Speech Recognition via Two-Pass Decoding](https://arxiv.org/pdf/2506.12154)
- [SPGISpeech 2.0: Transcribed multi-speaker financial audio](https://arxiv.org/html/2508.05554v1)
- [distil-whisper/earnings22 · Datasets at Hugging Face](https://huggingface.co/datasets/distil-whisper/earnings22)
- [A Complete Guide to Audio Datasets](https://huggingface.co/blog/audio-datasets)
- [Distil-Whisper: Robust Knowledge Distillation via Large-Scale Pseudo Labelling](https://arxiv.org/pdf/2311.00430)
- [MAEC: A Multimodal Aligned Earnings Conference Call Dataset](https://dl.acm.org/doi/10.1145/3340531.3412879)
- [ESB: A Benchmark For Multi-Domain End-to-End Speech Recognition](https://arxiv.org/pdf/2210.13352)
- [Contextual Earnings-22: A Speech Recognition Benchmark with Custom Vocabulary in the Wild](https://arxiv.org/html/2604.07354)