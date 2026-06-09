---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MLflow用户界面Nanochat训练运行
translated: true
type: note
---

MLflow UI 已启动并运行。以下是摘要：

---

**MLflow UI：http://localhost:5001**

该数据库包含来自 MI300X (amd-cloud) 的 nanochat 训练运行记录。内容如下：

**3 个实验，5 次运行：**

| 运行名称 | 状态 | 关键指标（最新步骤） |
|---|---|---|
| smoke-test | 已完成 | loss: 3.2 (步骤 1) |
| test-mi300x | 已完成 | loss: 10.40, mfu: 2.8%, tok/s: 7,009 (步骤 0) |
| test-mi300x-bs64 | 已完成 | loss: 10.40, mfu: 3.4%, tok/s: 8,292 (步骤 0) |
| mi300x-d24-760m | 运行中 | loss: 3.76, mfu: 27.1%, tok/s: 67,119 (步骤 200) |
| mi300x-d24-760m-fp8 | 运行中 | loss: 10.40, mfu: 6.8%, tok/s: 16,886 (仅步骤 0) |

**模型配置 (d24-760m 运行)：**
- depth=24, head_dim=128, max_seq_len=2048
- total_batch_size=524288, device_batch_size=32
- matrix_lr=0.02, embedding_lr=0.3, weight_decay=0.28
- warmup_steps=40, warmdown_ratio=0.65

**已应用修复：** 数据库是在 amd-cloud 上使用 mlflow 3.13.0（从源码构建）创建的，但 PyPI 上仅有 3.1.4 版本。已将 alembic_version 从 `da6fb0208061` 修补为 `bda7b8c39065`，以便本地 UI 能够读取。

注意：`mi300x-d24-760m` 运行显示了良好的进展——在 MI300X 上经过 200 步，loss 从 10.4 降至 4.87 再降至 3.76，MFU 为 27%。fp8 运行似乎卡在步骤 0，吞吐量低得多（16k tok/s 对比 67k）——可能是冷启动或 fp8 矩阵乘法在小规模下的开销所致。