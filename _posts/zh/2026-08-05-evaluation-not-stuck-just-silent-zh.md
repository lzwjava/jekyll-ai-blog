---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 评估未停滞，只是静默
translated: true
type: note
---

它**没有卡住**——评估正在正常运行。以下是证据：

**GPU + worker 正在活跃计算：**
```
GPU 利用率：73% → 64% → 75%（9 秒内轮询），内存稳定在 9887 MiB
Worker 子进程 44161：CPU 101%，RSS 1.95 GB，正在全力运算
```

**为什么看起来像卡住了——脚本没有每个样本的进度输出。** 查看 `base_evaluator.py` 中的代码流程：

1. `Loading weights: 100%` — 两个模型均已加载 ✅  
2. `Download complete: 0.00B` — 那是从 Hugging Face Hub 拉取 `kernels-community/finegrained-fp8` Triton 内核包（仅首次运行；0.00B 只是显示异常的进度条）  
3. 现在进入了 `run_dataset()` → `generate_one_sample()` 处理 gsm8k 数据集。循环中**没有 tqdm / 没有每个样本的打印输出**——结果只会在**每个数据集结束时**通过 `print_dataset_result()` 以表格行的形式出现。

因此屏幕上大约每 6 分钟（100 个样本 × 约 3.5 秒/样本）才会显示一条内容，例如：

```
+-------+--------------+-------------+--------+------+...+
| gsm8k | Qwen3-4B-FP8 | step_latest | ...    |      |
+-------+--------------+-------------+--------+------+...+
```

**时间预估：**
- gsm8k 行 → 约 6 分钟（你现在大约在第 3 分钟）
- math500 → 约 12 分钟
- humaneval → 约 18 分钟
- mbpp → 约 24 分钟
- alpaca → 约 30 分钟

在另一个终端查看进度的方法：
```bash
nvidia-smi -l 10                       # GPU 活动
ps -o pid,etime,time,%cpu -p $(pgrep -f spawn_main)   # worker CPU 时间增长
```

如果它真的卡住了，GPU 利用率会接近 0%，worker 的 CPU 也会保持不变。但实际情况并非如此。让它继续跑吧——第一个 gsm8k 行应该在大约 6 分钟时出现。下次如果你想要每个样本的进度，我可以给 `run_dataset()` 中的循环添加 `tqdm`。