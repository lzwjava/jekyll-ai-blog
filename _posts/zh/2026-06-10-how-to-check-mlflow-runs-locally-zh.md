---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何本地检查MLflow运行
translated: true
type: note
---

问题：如何像在Weights & Biases中查看运行一样，检查类似命令中的NanoChat训练运行的MLflow结果？

回答：

MLflow的工作方式与W&B不同——除非你运行MLflow服务器，否则它不会自动成为托管的Web仪表板。以下是如何检查你的运行：

---

### 1. 检查默认的MLflow位置

默认情况下，MLflow会在当前工作目录下的`mlruns`目录中本地记录运行（在你的情况下是`/root/nanochat/mlruns`）。你可以这样查看：

```bash
cd /root/nanochat/mlruns
ls
```

你会看到实验目录（`0`、`1`等），每个目录包含具有UUID样式的运行名称。在每个运行文件夹内，你会发现：

* `meta.yaml` → 基本元数据
* `params/` → 记录的参数
* `metrics/` → 记录的指标
* `artifacts/` → 保存的模型、输出

---

### 2. 在本地运行MLflow UI

MLflow有一个内置的Web UI。要在浏览器中查看你的实验：

```bash
cd /root/nanochat
mlflow ui
```

默认情况下，它会在 [http://127.0.0.1:5000](http://127.0.0.1:5000) 启动。如果你在远程服务器上运行此命令，可能需要端口转发：

```bash
ssh -L 5000:127.0.0.1:5000 user@remote-server
```

然后在本地浏览器中打开 `http://127.0.0.1:5000`。

---

### 3. 通过编程方式检查运行

你还可以使用MLflow的Python API检查指标和参数：

```python
import mlflow

# List all experiments
experiments = mlflow.list_experiments()
for e in experiments:
    print(e.name, e.experiment_id)

# List runs of an experiment
runs = mlflow.list_run_infos(experiment_id="0")  # replace with your experiment id
for r in runs:
    print(r.run_id, r.status)
```

---

### 4. 关于NanoChat集成的提示

* 确保命令中的 `--tracker=mlflow` 实际指向你想要的MLflow后端（默认是本地 `mlruns`）。
* 如果你想要一个更类似W&B的在线仪表板，你还可以将MLflow设置为记录到远程服务器或云存储。

---

简而言之：**MLflow主要是本地的，除非你启动其Web UI**，这与默认云托管的W&B不同。

你基本上可以在 `/root/nanochat` 中运行 `mlflow ui` 并打开网页来查看指标、参数和产物。

---

如果你愿意，我可以给你一个**单行命令，直接打开仅显示你的 `test-mi300x` 运行的MLflow UI**，这样你就不必浏览所有实验。

要我这样做吗？