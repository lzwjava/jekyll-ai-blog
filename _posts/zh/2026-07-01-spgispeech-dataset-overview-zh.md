---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SPGISpeech数据集概述
translated: true
type: note
---

## 它是什么

SPGISpeech 是一个包含 5,000 小时专业转录金融音频的语料库，内容为上市公司财报电话会议，由 Kensho Technologies（S&P Global 子公司）发布，相关论文为 [SPGISpeech 论文](https://arxiv.org/abs/2104.02014)（O'Neill 等人，2021）。它是 ASR 领域标准的“正式商务语音”基准——是 Hugging Face **ESB（端到端语音基准）** 中 8 个数据集之一，并出现在 `hf-audio/open_asr_leaderboard` 上，因此你读到的任何 Whisper/Conformer/wav2vec2 论文很可能都会报告其 WER。

## 为什么它对 ASR 训练有意义

- 转录文本是完整格式化的——包含大小写、标点符号以及非标准词汇的反规范化（例如 "twenty seventeen" → "2017"，"$5 million" 保留为数字加符号）。这与 LibriSpeech 风格的小写无标点语料库形成关键区别——它训练模型输出可直接发布的文本，而不仅仅是音标转录。
- 大约 50,000 名说话人——巨大的说话人多样性，涵盖广泛的 L1 和 L2 英语口音，混合了自发言语（问答）和叙述性言语（准备好的发言）。
- 原始通话使用 Gentle（一种双遍强制对齐器）分割为 5 到 15 秒的片段，边界通过 py-webrtc 语音活动检测进行细化。音频格式：单声道、16kHz、16 位——与 Whisper/wav2vec2/Conformer 原生期望的格式一致。
- 已知偏差：接近 90% 的说话人为男性——这在财报电话会议中是预期的（高管偏向男性），在评估公平性之前值得注意。此外，领域是正式/脚本化的，因此如果你希望模型处理非正式语音，则需要数据增强。

## 注意事项

1. **受限数据集。** 你必须在 HF 页面上接受 Kensho 的使用条款，`load_dataset` 才能正常工作——这不是简单的点击同意，而是一份限制重新分发和重新识别的法律协议。接受后，通过标准 HF 认证（`huggingface-cli login` 或 `HF_TOKEN` 环境变量）即可解锁下载。
2. **大小。** 总计 781 GB，但有三种训练配置，你无需全部下载：

| 子集 | 大小 |
| --- | --- |
| S | 22GB |
| M | 107GB |
| L | 530GB（M 的超集，而 M 是 S 的超集） |
| dev | 11GB |
| test | 11GB |

## 最小使用示例

```python
from datasets import load_dataset

# 使用 S 配置进行快速迭代/微调实验
spgi = load_dataset("kensho/spgispeech", "S")

sample = spgi["train"][0]
audio_array = sample["audio"]["array"]     # np.float32，16kHz 单声道
sampling_rate = sample["audio"]["sampling_rate"]
transcript = sample["transcript"]

# 仅加载 dev/test，不拉取任何训练集
spgi_test = load_dataset("kensho/spgispeech", "test")
```

鉴于你从零开始训练 GPT-2/MoE 的工作，如果你希望在不规则文本 ASR 上微调或评估 Whisper/Conformer 风格的编码器-解码器模型，这个数据集是一个不错的选择——标点符号和大小写的要求使得任务比纯音素转录更困难，更接近生产级听写或会议转录产品的需求。

参考资料：

- [kensho/spgispeech 数据集卡片](https://huggingface.co/datasets/kensho/spgispeech)
- [SPGISpeech 论文（arXiv:2104.02014）](https://arxiv.org/abs/2104.02014)
