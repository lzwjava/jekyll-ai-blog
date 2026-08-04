---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多GPU评估进度条
translated: true
type: note
---

完成。已在 `deepspec/eval/base_evaluator.py` 的 `run_dataset()` 中添加了每个样本的 `tqdm` 进度条：

```python
indices = range(self.global_rank, len(dataset), self.world_size)
for idx in tqdm(
    indices,
    desc=f"[rank {self.global_rank}] {dataset_name}",
    total=len(indices),
    position=self.global_rank,
    leave=False,
    disable=(self.global_rank != 0),
    unit="sample",
):
```

具体细节：

- **desc** 显示数据集和排名，例如 `[rank 0] gsm8k: 37%|███ | 37/100 [02:10<03:41, 3.54s/sample]`
- **total** = 该排名的实际样本份额（`len(range(rank, N, world_size))`），因此进度条在每个排名上正确显示 0→100%
- **position/disable** — 仅排名 0 渲染进度条；在多 GPU 运行时，其他排名不会与其冲突（且只有排名 0 的终端重要）
- **leave=False** — 每个数据集后进度条清除，保持表格行整洁
- 编译检查通过 ✅，环境中已有 tqdm 4.67.3

**注意：** 您当前正在运行的评估（PID 44088）已导入旧代码——此更改适用于下次启动。由于下次运行将是全新的开始，您可以 Ctrl+C 当前任务，或等待其完成，并在下次运行时看到新的进度条。

如果希望在下次完整运行前快速测试，可执行：

```bash
cd /mnt/data/DeepSpec
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py \
  --dataset gsm8k --num-samples 3 --max-new-tokens 128
```

您应该会看到 `[rank 0] gsm8k: ... 3/3 [~10s, ...s/sample]`，然后是结果表格。
