---
audio: false
generated: true
image: false
lang: zh
layout: post
title: StarCoderData语料库概述
translated: true
type: note
---

**问题：** 介绍一下 `bigcode/starcoderdata` —— 它是什么、包含什么内容、以及它的结构。

**答案：**

**它是什么**

`starcoderdata` 是用于训练 StarCoder 和 StarCoderBase 的精确训练语料库：包含 86 种编程语言的 783 GB 代码，外加 54 GB 的 GitHub Issues、13 GB 的 Jupyter Notebook（以脚本和文本-代码对两种形式）以及 32 GB 的 GitHub commits，总计约 2500 亿 token。StarCoderBase 在大约 1 万亿 token 上进行了训练（即在该数据上训练了约 4 个 epoch），而 StarCoder Python 变体则在 Python 子集上额外训练了 2 个 epoch。

这使得它成为理解“Codex 风格”预训练语料库实际样子的最佳开放产物——它是封闭实验室私下所做工作的完全公开版本。

**生成它的流水线（真正有趣的部分）**

它从 The Stack v1（通过许可证检测获得的宽松许可 GitHub 代码）开始，并按顺序应用以下步骤：

1. **语言选择** —— 根据数据量和流行度选择 86 种语言，外加配置/标记格式（JSON、YAML、Markdown）。
2. **质量过滤器** —— 每种语言特有的启发式规则：行长度限制、字母数字比例、字母 token 比率、自动生成文件检测，以及对数据密集型文件（长 JSON/YAML 会被激进地截断）的过滤。针对每种语言进行人工检查以调整阈值。
3. **近似去重** —— MinHash + LSH（Jaccard 系数约 0.85，5-gram shingles）。去重是影响最大的单一步骤；他们的消融实验显示，近似去重比仅精确去重效果要好得多。
4. **PII 编辑** —— 他们训练了一个 NER 模型（StarPII），基于标注数据集检测并掩盖姓名、电子邮件、密钥、密码、IP 地址，然后替换为 `<NAME>`、`<API_KEY>`、`<IP_ADDRESS>` 等 token（实际上就是你刚刚添加到自定义指令中的编辑策略，在语料库规模上应用）。
5. **去污染** —— 移除与 HumanEval、MBPP、APPS、GSM8K 测试集匹配的文件。
6. **退出机制** —— 通过“Am I in The Stack”工具请求移除的开发者仓库被删除。

**磁盘上的结构**

仓库根目录下每种语言一个目录（`python/`、`cpp/`、`rust/`、`java/`……共 86 个目录），每个目录包含 Parquet 碎片。代码行包含 `content`（源代码文本）、`id` 和 `max_stars_count`。四个特殊子集具有不同的模式，因此一次性加载整个数据集会失败——需要分别加载它们：`jupyter-scripts-dedup-filtered`、`jupyter-structured-clean-dedup`、`github-issues-filtered-structured`、`git-commits-cleaned`。

一个关键的格式细节：内容将元数据和结构嵌入为特殊 token，StarCoder 的 tokenizer 将其视为原子 token：

```
<reponame>owner/repo<filename>src/foo.py<gh_stars>42
... 实际代码 ...
```

Commits 看起来像 `<commit_before>...<commit_msg>...<commit_after>`，而 Issues 使用 `<issue_start>`、`<issue_comment>` 等。如果你在这个数据上训练自己的 tokenizer，需决定是否保留这些标记——它们是 StarCoder 学习仓库/文件条件生成的方式，并使得可以通过提示 `<gh_stars>1000` 来偏向更高质量补全的技巧成为可能。FIM（`<fim_prefix>/<fim_middle>/<fim_suffix>`）是在训练时应用的，而不是嵌入在数据集中。

**如何使用**

它是受限制的——你必须登录并接受 The Stack 的使用条款（下游使用必须尊重原始代码许可证；你同意传播移除请求更新）。然后：

```python
from datasets import load_dataset

# 流式加载一种语言；永远不要盲目下载全部 783GB
ds = load_dataset("bigcode/starcoderdata", data_dir="python",
                  split="train", streaming=True)

for i, row in enumerate(ds):
    print(row["content"][:300], "\n---")
    if i == 2: break
```

**根据你的配置进行规模估算：** 仅 `python/` 目录就约 60GB（约 200 亿 token）——对于一次 Chinchilla 最优的 760M 参数模型训练（约 150 亿 token）来说绰绰有余，它可以放在你工作站的 916GB 磁盘上，但不太适合放在 Air 上。对于 MI300X，最清晰的方式是流式加载 + 即时 tokenization 到内存映射的 `.bin` 文件（nanoGPT 风格的 `prepare.py`）；使用 `tiktoken` 对 200 亿 token 进行 tokenization 是一次性的 CPU 任务，大约需要 1-2 小时。TinyLlama-1.1B 使用了这个数据集作为其代码混合部分，因此它的仓库是你在当前规模下实现摄取流水线的良好参考。

注意：这是 *v1* 版本。如果你想要更新更大的版本，StarCoder2 对应的数据集是 `bigcode/the-stack-v2-train-smol-ids` / `-full-ids`（约 9000 亿 token，但内容必须从 Software Heritage S3 获取，如前所述）。对于首次训练运行，`starcoderdata` 的内联文本使其更加易用。

**参考资料：**

- [starcoderdata 数据集卡片](https://huggingface.co/datasets/bigcode/starcoderdata)
- [StarCoder: May the source be with you!（论文）](https://arxiv.org/abs/2305.06161)
- [The Stack: 3 TB of permissively licensed source code（论文）](https://arxiv.org/abs/2211.15533)
