---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SPGISpeech：完全格式化的端到端自动语音识别
translated: true
type: note
---

## 核心思想

标准ASR（语音转文本）系统预测的是*未格式化*文本——全小写、无标点、数字拼写（如"ninety two year history"）。要生成像"92-year history"这样可读的输出，通常需要独立的后续处理流程：大小写还原模型、标点恢复模型、逆文本标准化（ITN）模型，每个模型都需要独立训练和维护。

本文贡献两点：

1. **一个数据集**：SPGISpeech——5000小时财报电话会议音频，完全正字法转录（正确大小写、标点、"92-year"而非"ninety two year"），约50000位说话人，10万词汇量。它比此前任何达到此转录格式级别的语料库大约大10倍。
2. **一个任务框架**：直接训练声学模型以端到端方式输出完全格式化文本，而非在原始转录后串联格式化模型。

采用端到端（而非事后处理）的论据基于信息可用性：某些正字法决策确实需要声学信号，而不仅仅是文本。他们的例子——"the CEO retired"——句尾是`.`还是`?`可能取决于音高轮廓，一旦压缩为未格式化文本，这些信息就丢失了。因此，将标点恢复模型串联到纯ASR输出上，会丢弃声学模型原本拥有的信息。

## 架构（这部分与你对Transformer/注意力的兴趣相关）

他们训练的是**Conformer**模型——这是值得理解的关键技术点，因为你深入研究Transformer内部机制。

Conformer = Transformer编码器块 + 中间插入的卷积模块。直觉上：自注意力擅长捕捉长程/全局依赖关系，但在建模精细的*局部*模式方面较弱（这在音频中很重要——音素级转换在几十毫秒内发生）。深度可分离卷积子层弥补了这一点。

单个Conformer块大致如下：

```python
class ConformerBlock(nn.Module):
    def __init__(self, d_model, n_heads, conv_kernel=31, ff_mult=4):
        super().__init__()
        self.ff1 = FeedForward(d_model, ff_mult)          # 半步残差
        self.mhsa = nn.MultiheadAttention(d_model, n_heads, batch_first=True)
        self.conv = ConvModule(d_model, kernel=conv_kernel)  # 深度卷积 + GLU
        self.ff2 = FeedForward(d_model, ff_mult)           # 半步残差
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x, attn_mask=None):
        x = x + 0.5 * self.ff1(x)
        attn_out, _ = self.mhsa(x, x, x, attn_mask=attn_mask)
        x = x + attn_out
        x = x + self.conv(x)
        x = x + 0.5 * self.ff2(x)
        return self.norm(x)
```

卷积模块是深度可分离的，前面有一个GLU门——这是局部模式提取器：

```python
class ConvModule(nn.Module):
    def __init__(self, d_model, kernel=31):
        super().__init__()
        self.pointwise1 = nn.Conv1d(d_model, 2 * d_model, 1)
        self.glu = nn.GLU(dim=1)
        self.depthwise = nn.Conv1d(d_model, d_model, kernel,
                                    padding=kernel // 2, groups=d_model)
        self.bn = nn.BatchNorm1d(d_model)
        self.pointwise2 = nn.Conv1d(d_model, d_model, 1)

    def forward(self, x):  # x: (B, T, C)
        x = x.transpose(1, 2)
        x = self.glu(self.pointwise1(x))
        x = self.depthwise(x)
        x = F.silu(self.bn(x))
        x = self.pointwise2(x)
        return x.transpose(1, 2)
```

论文中两个模型变体：
- **Conformer (ESPnet)**：编码器-解码器，RNN-T风格（12个编码器块，6个Transformer解码器块，推理时自回归——速度较慢）。
- **Conformer-CTC (NeMo)**：相同编码器，但使用线性解码器 + **CTC损失**替代自回归解码器。非自回归 → 推理速度更快，因为整个输出序列在单次前向传播中通过单调对齐假设进行评分/解码。

关于CTC损失（它在概念上与基于token的交叉熵不同）：它通过对所有可能的对齐（较长的声学帧序列与较短的标签序列之间）进行边缘化，使用空白token允许重复/无输出帧，通过动态规划（前向-后向算法，与HMM前向-后向相同的DP结构）高效计算。如果你不熟悉这一点，值得理解——它与你在其他结构化预测设置中认识的"通过DP对所有对齐求和"的技巧相同。

两者都使用SentencePiece子词分词（约5000词汇量）而非原始字符——与LLM相同的分词理念，应用于ASR模型的输出端。

## 结果

在全格式化的正字法任务上，CER为1.7%（ESPnet Conformer）/ 1.8%（Conformer-CTC）。与相同输出的标准化词汇版本（小写、去除标点）比较，他们发现总错误中约一半到三分之二专门来自正字法决策（大小写、标点、去标准化）——即格式化确实很难，并非微不足道的附加项，这支持了他们的论点：它应该与声学到音素的映射联合学习，而非事后拼接。

## 这对你为何可能特别有趣

- 这里的CTC与自回归解码器权衡，与你处理LLM推理时的吞吐量/延迟权衡相同（并行解码 vs. 顺序采样）——值得与你已经考虑的KV缓存/推测解码权衡进行心理连接。
- 如果你从事任何与音频相关的智能体工作（语音界面、CLI智能体的转录流程），这是"让模型端到端完成整个任务"而非"专用模型流水线"的干净示例——直接符合你的AI原生偏好。
- 数据集本身（Kensho / S&P Global财报电话会议）是领域特定的（金融），这在主题上接近你的银行AI工程工作——如果你接触过通话转录或基于语音的金融科技工具。

参考文献：

- [SPGISpeech: 5,000 hours of transcribed financial audio for fully formatted end-to-end speech recognition (arXiv:2104.02014)](https://arxiv.org/pdf/2104.02014)