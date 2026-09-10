---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 下载Q4_K_M融合模型
translated: true
type: note
---

直接来自那个分支的答案：

| 仓库中的文件 | 可运行？ |
| --- | --- |
| `Qwen3.8-27B-Uncensored-<QUANT>.gguf`（融合版） | **是** - 独立运行，包含 MTP 头部 |
| `Qwen3.8-27B-Uncensored-noMTP-<QUANT>.gguf` | **是** - 独立运行，但需搭配草稿文件以提高速度 |
| `Qwen3.8-27B-Uncensored-draft-<QUANT>.gguf` | **否** - 这就是你有的文件。仅包含草稿头部 |
| `mmproj-Qwen3.8-27B-Uncensored-F16.gguf` | 否 - 视觉投影器，非模型文件 |

因此请下载**一个**融合文件。针对你的 RTX 4070（12 GB 显存，约 9.4 GB 可用）+ 62 GB 内存：

| 量化类型 | 大小 | 评估 |
| --- | --- | --- |
| `IQ2_M` | 10.6 GB | 精度损失过大（PPL 7.86 vs 7.18） |
| `IQ4_XS` | 15.3 GB | 效果好，显存余量最多 |
| **`Q4_K_M`** | **16.8 GB** | **最佳选择** - PPL 7.18，约 9 GB 显存 + 约 8 GB 内存 |
| `Q5_K_M` | 19.5 GB | 尚可，速度较慢 |
| `Q6_K` / `Q8_0` | 22-29 GB | 大部分依赖 CPU，速度明显较慢 |

获取文件的命令：

```bash
hf download JonathanColetti/Qwen3.8-27B-Uncensored-GGUF \
  Qwen3.8-27B-Uncensored-Q4_K_M.gguf \
  --local-dir /mnt/data/llama.cpp/models
```

然后：

```bash
cd /mnt/data/llama.cpp && ./build/bin/llama-server \
  -m models/Qwen3.8-27B-Uncensored-Q4_K_M.gguf \
  --spec-type draft-mtp --spec-draft-n-max 2 \
  -c 32768 -ngl auto --fit on \
  --host 127.0.0.1 --port 8080
```

网页界面位于 `http://127.0.0.1:8080`。

你现有的 `draft-Q8_0.gguf` 在融合文件中不再需要（MTP 头部已内置）。只有当你选择 `noMTP-*` 配合显式 `-md` 参数时才需要它。

要我现在下载 Q4_K_M 并启动吗？
