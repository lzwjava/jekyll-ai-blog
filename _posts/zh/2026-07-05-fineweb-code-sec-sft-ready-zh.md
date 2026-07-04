---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FineWeb代码SEC SFT就绪
translated: true
type: note
---

**SFT 流水线已就绪。** 以下是完整计划：

---

**`/mnt/data/zz/fineweb-code-sec-gpt/` 中的文件：**

```
├── prompt_*.txt                 # 13 个测试提示（代码/SEC/通用）
├── results.txt                  # 预训练模型的生成结果
├── prepare_sft_data.py          # 创建包含 1000 个代码+SEC 对话示例的 JSONL 文件
├── sft_code_sec.sh              # 在 d12 预训练模型上运行 SFT
└── run_prompts.py               # 从任意检查点生成样本
```

**SFT 的功能：**

- 使用我们的 **d12 模型**（第 50k 步，混合数据上的 val_bpb 为 1.418）
- 使用来自 **SmolTalk**（46 万条通用对话）+ **自定义代码/SEC**（1k 示例）+ **MMLU/GSM8K/Spelling**（推理）的对话进行微调
- 使用 BOS 对齐的 bestfit 打包和 **损失掩码**（仅训练助手令牌）
- **验证 BPB 在短短 7 步内从 1.418 降至 0.954**

**运行：**

```bash
bash /mnt/data/zz/fineweb-code-sec-gpt/sft_code_sec.sh           # 完整 SFT
bash /mnt/data/zz/fineweb-code-sec-gpt/sft_code_sec.sh --smoke   # 快速测试
```

**SFT 后，测试生成：**

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
python /mnt/data/zz/fineweb-code-sec-gpt/run_prompts.py --step 7 --temp 0.7
# SFT 检查点保存至 ~/.cache/nanochat/chatsft_checkpoints/d12/
```
