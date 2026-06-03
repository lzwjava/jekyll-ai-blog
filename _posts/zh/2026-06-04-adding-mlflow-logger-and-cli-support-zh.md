---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 添加MLflow日志记录器和CLI支持
translated: true
type: note
---

全部完成。以下是新增内容：

**在 lzw@192.168.1.36 上更改的文件：**

1. **`/mnt/data/nanochat/nanochat/mlflow_logger.py`**（新增）— `MLflowLogger` 类，提供与 wandb / DummyWandb 相同的 `.log()` / `.finish()` 接口。通过 `mlflow.log_metrics()` 记录数值指标，将字符串值记录为标签，配置记录为参数。

2. **`/mnt/data/nanochat/scripts/base_train.py`** — 新增 `--tracker {wandb,mlflow,none}`、`--mlflow-uri`、`--mlflow-experiment` 参数。移除了顶层的 `import wandb`（现在在 else 分支中惰性导入）。

3. **`/mnt/data/nanochat/scripts/chat_sft.py`** — 相同的 tracker 参数，相同的模式。

4. **`/mnt/data/nanochat/scripts/chat_rl.py`** — 相同的 tracker 参数，相同的模式。

5. **`/mnt/data/nanochat/pyproject.toml`** — 在依赖中添加了 `mlflow>=2.20.0`。

**用法：**

```bash
# 默认使用 wandb（行为不变）
python -m scripts.base_train --run=my-run

# 使用 MLflow 本地文件存储
python -m scripts.base_train --run=my-run --tracker mlflow

# 使用 MLflow 远程服务器
python -m scripts.base_train --run=my-run --tracker mlflow --mlflow-uri http://localhost:5000

# 不使用任何 tracker
python -m scripts.base_train --run=my-run --tracker none

# 查看结果
mlflow ui --port 5000
```

**Xiaomi API 密钥** 也在远程端修复了——现已与本机的密钥一致（51 个字符，`tp-cfmiit9...`）。
