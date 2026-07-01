---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 本地下载S配置
translated: true
type: note
---

不，目前尚未下载任何内容——上述所有读取操作都是通过 HF Hub 的远程文件系统（`HfFileSystem`）以流式方式进行的。`spgispeech/` 目录仅占 5.2 GB，而这实际上只是 Python 虚拟环境（torch 2.6+cu124 本身约 5 GB）。

**磁盘**：`/mnt/data` 上可用空间为 845 GB。

我们还有充足的存储空间。若要将实际的 parquet 文件下载到本地以实现即时读取，您可能需要：

- **S 配置**：约 45 GB（训练集 + 验证集 + 测试集）—— 快速
- **M 配置**：约 134 GB（仅训练集）—— 适中
- **L 配置**：约 580 GB（仅训练集）—— 体积较大但仍可容纳

想要下载其中一个吗？我建议选择 **S**（45 GB，轻松容纳，约 7.7 万个片段，足够用于微调实验）。如果您需要完整的 SPGISpeech 论文基准测试环境，还需要 **dev**（11 GB）和 **test**（11 GB）。

命令如下：

```bash
huggingface-cli download kensho/spgispeech --include "S/*" --local-dir /mnt/data/zz/spgispeech/data
```

或者使用 `hf download`（新版 CLI）。
