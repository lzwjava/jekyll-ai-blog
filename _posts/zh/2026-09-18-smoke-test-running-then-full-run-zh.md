---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 冒烟测试运行，然后全面运行
translated: true
type: note
---

冒烟测试**已经在运行中**，位于名为 `grpo` 的 tmux 会话中（我已终止了之前中止调用产生的重复进程）。以下是你需要的命令：

```bash
# 1. 查看冒烟测试日志（已在 tmux 会话 'grpo' 中运行）
tail -f /mnt/data/zz/grpo-rl/smoke.log

# 或附加到实时会话（退出附加：先按 Ctrl-b 再按 d）
tmux attach -t grpo
```

首次运行会将 `Qwen/Qwen2.5-1.5B`（约 3.1 GB）下载到 `~/.cache/huggingface`，然后执行 2 步优化器步骤。

一旦冒烟测试打印出 `Done - LoRA adapter saved`，即可开始正式运行：

```bash
tmux new-session -d -s grpo-full -c /mnt/data/zz/grpo-rl \
  './run.sh --num-epochs 2 2>&1 | tee full.log'

tail -f /mnt/data/zz/grpo-rl/full.log     # 监控
tmux attach -t grpo-full                  # 或附加
```

有用的覆盖参数（所有标志均见 `train_grpo.py --help`）：

```bash
./run.sh --model Qwen/Qwen2.5-3B --grad-accum 8     # 扩大规模，仍适配 12 GB 显存
./run.sh --dataset gsm8k                            # 真实数学题（已本地缓存）
./run.sh --beta 0.005 --temperature 1.2             # 若奖励出现平台期
./run.sh --resume                                   # 从上次检查点继续
```

在第三个面板中使用 `watch -n1 nvidia-smi` 监控显存 —— 若发生 OOM，将 `--max-completion-length` 降至 256 或 `--num-generations` 降至 2。

在 `/mnt/data/zz/grpo-rl/` 下创建的文件：

| 文件 | 用途 |
| --- | --- |
| `train_grpo.py` | GRPO 训练器，argparse 命令行接口，已针对 TRL 1.13 修复 |
| `run.sh` | 正式训练配置（包含 `smoke` 模式） |
| `setup_env.sh` | venv 创建 + 依赖安装（已执行） |
| `requirements.txt` | 锁定版本 |

相对于原始代码片段的三处修复，运行期间可关注：

1. TRL 1.13 中不再有 `max_prompt_length`，且 `torch_dtype`/`eval_strategy` 已重命名 —— 脚本使用了当前 API。
2. 奖励现在拆分为**两个函数**（`reward_format`、`reward_correctness`），TRL 会分别记录 —— 可观察提升来自格式还是实际正确性。
3. 缺少 `prepare_model_for_kbit_training` + `gradient_checkpointing_kwargs={"use_reentrant": False}`；没有它们 QLoRA + checkpointing 不稳定。注意力默认使用 `sdpa`（未安装 flash-attn，1.5B 规模下也无必要）。
