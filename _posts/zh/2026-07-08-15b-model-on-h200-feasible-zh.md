---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 1.5B模型在H200上可行
translated: true
type: note
---

## 1.5B 模型在 H200 上的可行性分析

**是的，可行。** 基于代码库分析：

### 参考（MI300X）：`760M` 在 batch=32 时 → 105 GB / 192 GB

### H200 优势：
- **FA3**（Flash Attention 3）—— 相比 AMD 上的 SDPA，激活内存大幅降低
- **FP8** 支持 —— 矩阵乘法内存可减半
- 更高的 MFU（约 45% 对比 27%）

### 建议的 ~1.5B 配置

| 参数 | 值 | 说明 |
|-------|-------|-------|
| `--depth` | **30** | base_dim=1920, model_dim=1920（整齐的 15×128 头） |
| `--aspect-ratio` | 64 | 标准 |
| `--head-dim` | 128 | FA3 最佳点 |
| `--device-batch-size` | **16** | MI300X 的一半，以适配 140 GB 对比 192 GB |
| `--total-batch-size` | 524288 | 与参考相同 |
| `--max-seq-len` | 2048 | 标准 |
| `--window-pattern` | SSSL | 交替滑动窗口 |
| `--fp8` | 可选 | 节省约 40% VRAM，H200 支持 |

**参数量：** 约 1.45B（30 层 × 1920 维度 × 15 头）
**Chinchilla 最优数据量：** 约 29B tokens（20 倍参数量）—— 适配我们的 35.8B tokens 数据集
**训练步数：** 约 55,000 步（每步 524K tokens）
**预估 VRAM：** 约 110-120 GB（使用 FA3，batch=16）—— 适配 140 GB
**使用 FP8：** 约 80-90 GB —— 非常宽裕

### 命令

```bash
cd /workspace/zz
tmux new -s train-1.5b
python -m scripts.base_train \
  --depth=30 \
  --device-batch-size=16 \
  --total-batch-size=524288 \
  --max-seq-len=2048 \
  --window-pattern SSSL \
  --target-param-data-ratio=20 \
  --eval-every=500 \
  --save-every=5000 \
  --run=h200-d30-1.5b \
  --tracker=wandb
```

需要我运行它吗？