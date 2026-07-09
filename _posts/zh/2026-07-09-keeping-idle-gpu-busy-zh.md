---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 让闲置GPU保持忙碌
translated: true
type: note
---

RTX 4070, 12GB — 处于 **0% 利用率**，P8 空闲状态，功耗 13W（最大 215W）。llama-server 占用约 5.9GB 但无任务（空闲）。剩余约 4.8GB 可用。

以下是让它忙起来的有用方法，按与你技术栈的匹配程度排序：

---

### 1. 批量推理 / 评估（最实用）

如果 llama-server 只是闲置，那就给它分配任务。在模型上运行评估框架，或者通过服务器批量处理数据集。

```bash
# 将 llama-server 指向评估任务
# 或者在数据集上运行批量推理
curl http://localhost:8080/v1/chat/completions \
  -d '{"model":"gemma-4","messages":[{"role":"user","content":"hello"}],"max_tokens":100}' > /dev/null
```

你可以设置一个 cron 任务，每晚运行评估框架：

```bash
# ~/.hermes/cron/ 或系统 cron
hermes cron create --name "nightly-eval" --schedule "0 2 * * *" \
  --prompt "在 /mnt/data/models/gemma-4-... 上运行 lm-eval-harness 并报告结果"
```

### 2. 后台 LLM 服务（它已经在做了，但可以调优）

llama-server 处于 P8 状态且利用率为 0%，说明已加载但无人查询。如果你想让它 *有用* 地忙起来——让你自己的 CLI 代理（`ww`、`zz`）通过它而不是 OpenRouter 来服务。这样可以节省 token 并保持 GPU 活跃。

### 3. LoRA 微调（无监督）

在你睡觉时，对关心的数据集训练 LoRA 适配器：

```bash
# unsloth + TRL — 轻松适配 12GB
python3.11 -m unsloth.train \
  --model /mnt/data/models/gemma-4-E4B-it-Q3_K_M.gguf \
  --dataset your-dataset \
  --output_dir /mnt/data/lora-runs/cool-experiment
```

剩余 4.8GB 对于完整的 GPT-2 124M+ 训练来说很紧张，但 LoRA/Q-LoRA 在较小模型上轻松适配。

### 4. Fold@home / BOINC（公益计算）

如果你想要零后台工作量的忙碌：

```bash
# Folding@home — 为蛋白质折叠研究做贡献
apt install -y foldingathome
FAHClient --user=lzw --team=0 --gpu=true
```

功耗约 50W，以低优先级运行，不影响交互工作。

### 5. 数据集生成 / 合成数据

利用空闲 GPU 生成合成训练数据：

```bash
# 通过 llama-server 批量 API 提交大量提示列表
# 生成 QA 对、偏好数据、代码示例
python3.11 << 'EOF'
# 从文件读取提示，发送批量请求到本地 llama-server
# 将结果存储为 JSONL
EOF
```

---

你追求的“忙碌”是哪种类型？

- **有用的忙碌** — 批量推理、评估、数据集生成、LoRA 训练
- **后台忙碌** — Fold@home/BOINC、持续评估基准测试
- **基准测试忙碌** — 用压力测试烧机以验证稳定性

选择一种模式，我可以搭配正确的命令和 cron 集成来配置它。