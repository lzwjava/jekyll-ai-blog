---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Python 3.12的冒烟测试通过
translated: true
type: note
---

端到端烟雾测试在系统 Python 3.12 上成功运行。✅

**结果：**
- **make_synthetic** → `data/synthetic/{en,zh,aligned}.jsonl`
- **mix_bilingual** → 2000 个文档，英文 50% / 中文 50% → `mixed.txt`
- **train_tokenizer** → 联合分词器，词表大小=357，添加控制标记 → `tok_mixed/`
- **measure_token_ratio** → 写入 `ratios.json`（中文约占 38.8% 的 token——证实了 README 中的陷阱：文档比例 ≠ token 比例）
- **prepare** → `data/train.bin`（90KB）+ `data/val.bin`（10KB）

我使用了与项目自身 pycache 文件（`cpython-312`）期望一致的 Python 3.12 调用方式（`python3.12 -m scripts.<name>`）。完整流水线正常运行。

**注意：** 这覆盖了 `mixed.txt`（现在约 100KB 的合成数据，之前为空）以及 `tok_mixed/` 中的合成分词器。当你转移到真实的 3.5GB `fineweb_edu_shard.jsonl` 时，需要重新运行真实流水线（下载中文分片，大规模混合，训练一个完整的 65536 词表分词器）。需要我启动这个流程，或者运行生成步骤吗？