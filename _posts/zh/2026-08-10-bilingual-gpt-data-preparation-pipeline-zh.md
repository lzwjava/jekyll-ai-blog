---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 双语GPT数据准备流水线
translated: true
type: note
---

这是一个**用于从头训练双语（英文/中文）GPT 的数据预处理管道**。以下是端到端的工作流程：

## 核心思路

你不能仅仅在一堆混合的中英文文本上训练，然后期望在生成时控制模型使用哪种语言。本仓库的技巧：**为每个文档添加一个控制标记**（与 CTRL 控制码 / NLLB 语言标记相同的技巧），从而使语言选择成为一个模型需要学习的*条件*。

```
<|lang_zh|>
{text}
<|endoftext|>
```

在推理时，只需在提示前添加 `<|lang_zh|>`，模型就会保持中文输出；添加 `<|lang_en|>` 则会保持英文输出。

## 管道（每个脚本对应一个阶段）

```
en.jsonl ─┐
          ├→ mixed.txt ─→ tok_mixed/* ─→ data/train.bin / val.bin
zh.jsonl ─┘     (文档      (全新联合     (令牌,
                被包裹     字节级        nanoGPT
                在标记中)  BPE)         .bin 格式)
```

1. **`download_shards.py`** — 从 HuggingFace 各拉取一个分片：`fineweb-edu`（英文）和 `fineweb-2` 的 `cmn_Hani`（中文，普通话，简体），并将两者归一化为 `{"text": ...}` 的 jsonl 格式，以便一个混合器可以处理两者。

2. **`mix_bilingual.py`** — 语言比例旋钮。对于每个文档，掷硬币：以概率 `--zh-frac` 从中文分片抽取，否则从英文分片抽取。每个文档会被包裹上 `<|lang_zh|>`/`<|lang_en|>` 和 `<|endoftext|>` 后写入。

3. **`measure_token_ratio.py`** — *重要陷阱*：`--zh-frac` 是**文档**比例，而非**令牌**比例。中文每字节文本生成的令牌数更少，因此 50/50 的文档拆分可能按令牌计算只有约 39% 的中文（这正好是你的 `ratios.json` 显示的结果：`zh_doc_frac = 0.50` 但 `zh_token_frac = 0.39`）。该脚本对语料库进行分词，并报告实际的令牌构成，以便你可以调整 `--zh-frac` 直到*令牌*比例匹配。

4. **`train_tokenizer.py`** — 训练一个**全新的联合字节级 BPE**，并将控制标记注册为特殊标记（这样它们永远不会被拆分）。这是有意为之：GPT-2 的分词器将中文拆分为每个字符约 3 个令牌，浪费了上下文；在混合语料上训练全新的 BPE 可以学习真正的中文合并。

5. **`prepare.py`** — nanoGPT 的经典步骤：一次性将所有内容分词，按 90/10 分割，写入 `train.bin`/`val.bin` 的 `uint16` id（如果词表大小超过 65536，则切换到 `uint32`）。这些文件可以直接被 [nanoGPT](https://github.com/karpathy/nanoGPT) 训练。

6. **`generate.py`** — 收获成果。加载训练好的 nanoGPT 检查点和分词器，预置语言标记（或 `--mix-frac` 旋钮），然后进行采样。

## 可选的第二个旋钮（连续混合）

`build_codeswitch.py` 超越了纯英文/纯中文。给定一个**句子对齐的平行语料库**（例如 WMT 中英文），它以目标比例 `r` 交错排列英文和中文句子，并将文档标记为 `<|mix_0|>` … `<|mix_100|>`。然后 `--mix-frac 0.75` 告诉模型“这里大约 75% 是中文”——它会生成真正的代码混用输出。README 指出真正的限制在于数据（句子对齐的平行文本），而非模型。

## 仓库当前状态

- 一个完整的 3.5 GB `fineweb_edu_shard.jsonl` 英文分片已下载并位于仓库根目录（`ratios.json` 显示你已使用合成数据进行了烟雾测试：2000 个文档，约 28k 令牌）。
- 烟雾测试后已生成 `data/train.bin` + `val.bin` 以及一个 `tok_mixed/` 分词器（词表大小 2048）。
- `config/` 目录为空——尚未编写任何训练配置，也未进行任何训练（下一步：将 nanoGPT 配置指向 `data/` 并运行训练循环）。

是否需要我详细讲解任一特定部分，或者我应该运行合成烟雾测试来展示管道的端到端工作流程？
