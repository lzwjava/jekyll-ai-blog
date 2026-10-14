---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ZeRO第3阶段已实现并测试
translated: true
type: note
---

已完成。**ZeRO stage 3 已实现、测试并提交。** 最终状态：`45 通过，2 跳过`（之前为 36+2），示例可在 1 和 2 个 rank 上使用 `--zero 3` 进行训练和恢复。

## 构建内容

**设计** — stage 3 对*所有内容*进行分区，复用了现有的 stage-2 梯度路径：

| 状态 | 步骤之间（常驻） | 计算期间 |
| --- | --- | --- |
| fp32 主参数 | 仅 `1/N` 分片 | 每组的瞬态完整缓冲区，聚集后立即释放 |
| Adam 动量 | `1/N`（如 stage 1/2） | — |
| 梯度 | `1/N` reduce-scatter 分片 | 完整扁平缓冲区仅存在于从 flatten 到 reduce-scatter 期间 |
| 模型参数 | 每个参数的扁平 `1/N` 占位符切片 | 完整张量，在窗口的第一次 `engine(x)` 时全部收集 |

生命周期：`engine(x)` → `gather_parameters()`（每组一次 all-gather + fp32→fp16 转换）→ 前向/反向 → 边界：flatten → reduce-scatter → **释放梯度** → 裁剪（精确，分片平方和）→ 对分片执行 Adam → **释放参数**（占位符从更新的主参数刷新）。

## 文件

- **`minispeed/flat.py`** — `partition_params` / `materialize_params` / `dematerialize_params`、`master_range`、覆盖感知的重叠拷贝（适用于完整参数*和*部分占位符）、可延迟/可释放的梯度缓冲区
- **`minispeed/zero/stage_3.py`** *(新文件)* — `ZeROStage3Optimizer`：收集/释放/同步 + stage-2 减少，在 reduce-scatter 后丢弃完整梯度缓冲区
- **`minispeed/zero/__init__.py`** — `build_zero_optimizer` 工厂函数
- **`minispeed/engine.py`** — 初始化时分区，`forward` 中延迟收集，每个边界后释放（包括溢出跳过），收集感知的 `state_dict`/`load_state_dict`，新增 `gather` 计时器
- **`minispeed/checkpoint.py`** — 保存/加载时收集，恢复参数到加载前的状态
- **`minispeed/config.py`** — 接受 stage 3；拒绝 `stage3_gather_16bit_weights_on_model_save: false`（布局始终写入完整权重）；offload 仍然快速失败
- **测试** — 新增 `test_zero3.py`（6 个测试：stage3≡stage0、收集/释放生命周期、分区往返、溢出跳过、检查点重放、评估重新收集）；将 stage 3 添加到 `test_distributed`、`test_gpu`（gloo/CUDA fp32+fp16）、`test_config`
- **README / 示例 / 文档字符串**已更新（功能表、“四行 ZeRO”、步骤图、限制说明）

## 测试中发现的问题

1. 占位符索引假设 `p.data` 覆盖整个参数 — 已通过覆盖感知的 `_pdata_range()` 窗口修复。
2. `dematerialize_params` 对 rank 分片之外的参数生成了负大小 — 已增加保护。
3. **真正的问题**：示例中仅 rank-0 的采样演示死锁，因为 stage-3 前向是*集体操作* — 已修复示例并在 README 中记录了注意事项。

两个提交：`b839f9d`（功能）和 `9afccd9`（采样修复）。工作树干净。
