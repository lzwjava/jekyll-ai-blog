---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MLflow 集成完成
translated: true
type: note
---

无需更改任何代码。该集成已在代码库中完成。原因如下：

**CLI 参数**（base_train.py 第 43-45 行）：已定义：

- `--tracker`，可选值 `wandb|mlflow|none`
- `--mlflow-uri`，用于远程服务器
- `--mlflow-experiment`，用于实验名称

**初始化逻辑**（第 101-110 行）：已处理切换：

```python
if args.tracker == "mlflow":
    wandb_run = MLflowLogger(...)
```

**训练循环**：所有日志记录均通过 `wandb_run.log(...)` 进行，该函数对 wandb 和 MLflow 日志记录器（相同接口）均适用。

**MLflowLogger 类**：已实现 `log()` 和 `finish()` 方法——数值指标会记录为指标，字符串变为标签，配置记录为参数。

因此，只需在现有训练命令中添加以下三个标志即可：

```
--tracker=mlflow --mlflow-experiment=<名称> --run=<运行名称>
```

其他所有内容（每 N 步的验证 bpb、每 100 步的训练损失、CORE 指标、检查点）均通过相同的 `wandb_run.log()` 调用进行，并由 MLflow 自动捕获。
