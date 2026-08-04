---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 全新评估重试
translated: true
type: note
---

我之前的启动尝试因工具调用被终止，所以现在没有任务在运行——一切重新开始。以下是经过验证的准确命令：

```bash
cd /mnt/data/DeepSpec
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py \
  --dataset gsm8k,math500,humaneval,mbpp,alpaca \
  --num-samples 100 \
  --max-new-tokens 128
```

或者作为后台任务运行并记录日志：

```bash
cd /mnt/data/DeepSpec
nohup bash -c 'CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py --dataset gsm8k,math500,humaneval,mbpp,alpaca --num-samples 100 --max-new-tokens 128' > /tmp/eval_big.log 2>&1 &
tail -f /tmp/eval_big.log   # 用于查看进度
```

已验证的部分：
- `/usr/bin/python3.12` ✅ 存在，torch 2.11.0 + CUDA 工作正常，1 张 GPU
- 草稿检查点 ✅ `/home/lzw/checkpoints/deepspec/dspark_block7_qwen3_4b_fp8_toy/step_latest/`
- GPU 空闲（已使用 2592 MiB），无残留进程
- 所有参数与 `toy_run/eval_smoke.py` 一致

提醒：500 个样本预计需要约 30 分钟，之前运行中约 7% 的数字很可能是 `--max-new-tokens 128` 导致的截断伪影——不要将其视为真实的质量指标。