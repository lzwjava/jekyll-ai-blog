---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 令牌ID不匹配阻止数据重用
translated: true
type: note
---

**问题：** 为什么 nanochat 不能复用磁盘上已分词的 FineWeb-Edu 数据，而必须使用原始 parquet 格式加上全新的自定义分词器？

**答案：**

因为令牌 ID 在不同分词器之间不可移植，且 nanochat 的模型架构硬编码绑定到了自身的词表。

**1. 嵌入表是一个固定大小的查找表，键值绑定到特定词表**

```python
# nanochat 的 GPT 模型初始化（摘自 nanochat/gpt.py 的改写）
self.transformer.wte = nn.Embedding(vocab_size, n_embd)  # 例如 65536 x d_model
self.lm_head = nn.Linear(n_embd, vocab_size, bias=False)
```

这里的 `vocab_size` 来源于 nanochat 自行训练的分词器（`rustbpe`，大致相当于 tiktoken 风格的 BPE，默认约 65536 个合并）。而你现有的 `.npy` 文件是使用 **GPT-2 的 tiktoken**（`gpt2` 编码，词表容量 50257）进行分词的。在 GPT-2 BPE 下，令牌 ID `464` 代表 `"The"`。而在 nanochat 新训练的 BPE 下，ID `464` 则是根据语料统计结果任意生成的某个合并单元——它可能毫无意义，或者代表其他内容。你不能将一个分词器的 ID 输入到另一个为不同分词器 ID 空间构建的模型嵌入表中。这不是格式不匹配的问题，而是语义不匹配——这些整数不再指向相同的字符串。

**2. nanochat 将训练自身分词器作为显式的流水线步骤，而非可选配置**

```bash
# nanochat 实际流水线顺序
python -m nanochat.dataset -n 240          # 下载原始 parquet 分片
python -m scripts.tok_train --max_chars=... # 在*原始文本样本*上训练 BPE
python -m scripts.tok_eval                  # 检查压缩比是否合理
python -m scripts.base_train                # 预训练，使用刚训练好的分词器进行实时分词（或预分片）
```

`tok_train.py` 需要原始 UTF-8 文本，而非现有的整数数组，因为 BPE 合并学习过程需要基于原始字符串中的字节对进行。你的 `.npy` 文件已将文本转换为 GPT-2 的 ID——这一过程是有损/单向的，你无法通过“反分词” GPT-2 的 ID 来获得 nanochat 分词器训练所需的兼容数据，除非重新解码为文本（这确实可行——GPT-2 分词器是可逆的），但这样做反而会产生解码+重新分词的额外开销，且相较于直接使用原始 parquet 没有任何优势。

**3. 为什么 Karpathy 采用这种设计，而非复用 tiktoken/gpt2**

nanochat 自建分词器阶段的目的是为了教学/可控——词表大小、特殊令牌（`<|bos|>`、工具调用令牌等）以及合并行为都针对 nanochat 特定的聊天格式和训练方案进行了调优。该设计并非为了替换现成分词器；`gpt.py` 中所有关于 d-model/vocab_size/rotary-embedding 的配置都假设你已先运行了他们的分词器阶段。

**因此，你具体有两种选择：**

- **方案 A：** 保留（不要删除）原始 FineWeb-Edu parquet 文件，训练 nanochat 的分词器并在该语料上重新分词，跳过 ClimbMix 的下载——可节省 60GB 的 ClimbMix 下载量，但会失去 nanochat 作者验证过损失曲线的“配方匹配”数据质量/混合比例。
- **方案 B：** 完全删除 FineWeb-Edu，按照 nanochat 默认配方的要求下载 ClimbMix——与已发布的训练运行完全一致（可复现的损失曲线、已知良好的超参数），代价是 60GB 下载量及带宽/时间。

考虑到你正在进行 1.5B 参数规模的训练，且希望获得与已知 nanochat 基准测试相匹配的结果，而非调试自己的数据混合效果，**方案 B 是更安全的选择**——为了复用旧数据而进行优化，不值得在你试图验证与参考实现一致性的训练过程中引入干扰变量。

如果你需要，我可以将实际的 `du -sh`、`rm`、`uv venv` 以及分词器训练序列整合成一个脚本，这样你就不必手动一步步操作了。
