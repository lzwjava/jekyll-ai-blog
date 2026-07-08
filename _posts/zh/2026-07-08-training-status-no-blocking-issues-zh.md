---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练状态：无阻塞问题
translated: true
type: note
---

## 遇到的障碍及当前状态

### 1. 缺少 Python 开发头文件  ✅ 已修复
**症状**：Triton 启动时崩溃——`gcc` 无法编译 `cuda_utils.c`，因为 Python 3.10 缺少 `Python.h`。
**修复**：`apt-get install python3.10-dev`
**根本原因**：`uv sync --extra gpu` 使用 Python 3.10 创建了虚拟环境，但系统只安装了 Python 3.11 的开发头文件。

### 2. 磁盘空间不足  ✅ 已修复
**症状**：`/workspace` 仅剩 16G 空闲——不足以支持训练和检查点。
**修复**：删除了过时的 tokenized .npy 文件（67G）+ 重复的数据集目录（8.9G）。现在有 176G 空闲。

### 3. uv 同步超时  ✅ 已解决（用户自行运行）
**症状**：`uv sync --extra gpu` 在 600 秒时超时——torch 2.9.1+cu128 下载量较大。
**解决方法**：用户自行运行了该命令。

### 4. FA3 的 `flash_attn` 在测试中不可调用  ⚠️ 非阻塞
**症状**：直接调用 `flash_attn(q, k, v)` 失败，报错 `'SimpleNamespace' object is not callable`。
**为什么没问题**：训练中成功使用了它（参见 128K tok/s, 62% MFU）。直接 API 调用是封装问题——实际注意力内核通过 GPT 模型的代码路径工作。FA3 在启动时会打印 `✓ Using Flash Attention 3 (Hopper GPU)`。

### 5. Wandb 离线模式  ⚠️ 注意事项
**症状**：指标记录到 `wandb/offline-run-*`，未同步到云端。
**解决方法**：稍后运行 `wandb sync /workspace/nanochat/wandb/offline-run-<id>`，或使用 `WANDB_MODE=online` 并登录 wandb 账户重新运行。

### 6. FineWeb-Edu ≠ ClimbMix-400B  ⚠️ 数据质量差距
**问题**：nanochat 的速度记录（1.65 小时达到 GPT-2）使用的是 ClimbMix-400B，这是一个经过更好筛选的数据集。FineWeb-Edu 较旧且质量较低——预计最终损失/CORE 分数会略差。
**缓解措施**：我们有 35.7B 个 token——足以满足 d24（15.2B）和 d30（29B）的需求。结果会不错，但并非最优。

### 7. FP8 API 检查失败但训练正常  ⚠️ 非阻塞
**症状**：`torch.cuda.is_fp8_supported()` 报错（此 torch 构建版本未暴露该 API）。
**实际情况**：训练显示 `✓ FP8 training enabled (tensorwise scaling) - converted 145/158 linear layers`——FP8 通过自定义的 `fp8.py` 模块在 H200 硬件上正常工作，而非通过标准 torch API。

---

### 当前训练健康状况

| 检查项 | 状态 |
|--------|------|
| Triton 编译 | ✅ 正常工作 |
| H200 上的 FA3 | ✅ 已激活 |
| FP8 矩阵乘法 | ✅ 已启用（145 层） |
| 数据加载 | ✅ 44 个 parquet 文件，流式加载 |
| 损失曲线 | ✅ 平稳下降：第 108 步从 10.4 降至 4.9 |
| 吞吐量 | ✅ ~128K tok/s |
| MFU | ✅ ~62%（单 GPU 下表现优秀） |
| 预计完成时间 | ~33 小时总时长，剩余 ~32 小时 |

**总结**：没有阻塞性问题。训练将在 FineWeb-Edu 上完成并取得良好结果。对于此后的 **1.5B（d30）运行**，可以考虑下载 ClimbMix-400B 以获得更高质量，或使用 `--depth=30` 扩展相同流程。