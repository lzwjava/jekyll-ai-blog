---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向nanoGPT的双语语料库流水线
translated: true
type: note
---

这是一个 **Python** 数据预处理项目（非 Node）。它是一个用于 nanoGPT/nanochat 的中英双语语料库处理流水线。以下是运行命令：

**首先，安装依赖：**

```bash
pip install -r requirements.txt
```

**选项 A — 冒烟测试（无需下载），验证运行的最快方式：**

```bash
python -m scripts.make_synthetic       --out_dir data/synthetic
python -m scripts.mix_bilingual        --en data/synthetic/en.jsonl --zh data/synthetic/zh.jsonl --zh-frac 0.5 --out mixed.txt --limit 2000
python -m scripts.train_tokenizer      --input mixed.txt --out-prefix tok_mixed --vocab-size 2048
python -m scripts.measure_token_ratio  --input mixed.txt --out ratios.json --tok-prefix tok_mixed
python -m scripts.prepare              --input mixed.txt --tok-prefix tok_mixed --out-dir data
```

**选项 B — 实际流水线。** 注意你磁盘上已有 3.5GB 的 `fineweb_edu_shard.jsonl`，但 `mixed.txt` 当前为空（0 字节），尚未进行混合。执行：

```bash
# 1. 获取中文分片（你已有英文分片）
python3.12 -m scripts.download_shards --source zh --out fineweb2_cmn_shard.jsonl

# 2. 使用语言比例调节旋钮混合中英文
python -m scripts.mix_bilingual \
    --en fineweb_edu_shard.jsonl \
    --zh fineweb2_cmn_shard.jsonl \
    --zh-frac 0.50 --out mixed.txt --seed 0

# 3. 检查实际 token 比例，根据需要调整 --zh-frac
python -m scripts.measure_token_ratio --input mixed.txt --out ratios.json --tok-prefix tok_mixed

# 4. 训练联合双语 BPE
python -m scripts.train_tokenizer --input mixed.txt --out-prefix tok_mixed --vocab-size 65536

# 5. 分词 -> 二进制训练/验证集
python -m scripts.prepare --input mixed.txt --tok-prefix tok_mixed --out-dir data
```

**训练完成后，使用语言控制生成：**

```bash
python -m scripts.generate --model out/ckpt.pt --tok-prefix tok_mixed --lang zh \
    --prompt "机器学习是什么？" --max-new-tokens 200
```

---

**快速入门建议：** 从 **选项 A** 开始——冒烟测试几秒内即可端到端运行，在投入处理 3.5GB 大分片之前先确认工具链正常。然后再进入选项 B 处理真实语料。如果你告诉我你的目标（例如“仅验证运行”或“生成一个小的 train.bin 进行训练”），我可以给你一个组合命令。
