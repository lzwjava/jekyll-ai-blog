---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最大化闲置GPU利用率
translated: true
type: note
---

RTX 4070, 12GB — 处于 **0% 利用率**，P8 空闲状态，功耗 13W（最大 215W）。llama-server 占用约 5.9GB 但无操作（空闲）。剩余约 4.8GB 可用。

以下是有用的方式让它忙碌起来，按与你技术栈的契合度排序：

---

### 1. 批量推理 / 评估（最实用）

如果 llama-server 闲置，可以向它分配任务。在你的模型上运行评估工具，或通过服务器批量处理数据集。

```bash
# 让 llama-server 处理评估任务
# 或对数据集运行批量推理
curl http://localhost:8080/v1/chat/completions \
  -d '{"model":"gemma-4","messages":[{"role":"user","content":"hello"}],"max_tokens":100}' > /dev/null
```

你可以设置一个定时任务，每天夜间运行评估工具：

```bash
# ~/.hermes/cron/ 或系统 cron
hermes cron create --name "nightly-eval" --schedule "0 2 * * *" \
  --prompt "Run lm-eval-harness on /mnt/data/models/gemma-4-... and report results"
```

### 2. 后台 LLM 服务（它已经在做，但可以调优）

llama-server 处于 P8 状态且 0% 利用率，说明已加载但无人查询。如果你希望它 *有用* 地忙碌——通过它来服务你的 CLI 代理（`ww`、`zz`），而不是通过 OpenRouter。这样可以节省 token 并保持 GPU 活跃。

### 3. LoRA 微调（无监督）

在你睡觉时，在你关心的数据集上训练一个 LoRA 适配器：

```bash
# unsloth + TRL — 轻松适配 12GB
python3.11 -m unsloth.train \
  --model /mnt/data/models/gemma-4-E4B-it-Q3_K_M.gguf \
  --dataset your-dataset \
  --output_dir /mnt/data/lora-runs/cool-experiment
```

4.8GB 空闲对于完整 GPT-2 124M+ 训练来说有些紧张，但 LoRA/Q-LoRA 在较小模型上可以轻松运行。

### 4. Fold@home / BOINC（公益计算）

如果你想要零成本的后台忙碌：

```bash
# Folding@home — 为蛋白质折叠研究贡献力量
apt install -y foldingathome
FAHClient --user=lzw --team=0 --gpu=true
```

功耗约 50W，低优先级运行，不影响交互式工作。

### 5. 数据集生成 / 合成数据

利用空闲 GPU 生成合成训练数据：

```bash
# 通过 llama-server 批量 API 输入大量提示列表
# 生成问答对、偏好数据、代码示例
python3.11 << 'EOF'
# Read prompts from file, send batch to local llama-server
# Store results as JSONL
EOF
```

---

你想要哪种“忙碌”？

- **有用的忙碌** — 批量推理、评估、数据集生成、LoRA 训练
- **后台忙碌** — Fold@home/BOINC、持续评估基准测试
- **基准忙碌** — 用压力测试烧录以验证稳定性

选择一种模式，我可以为你配置相应的命令和 cron 集成。
