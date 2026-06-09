---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Check MLflow Runs Locally
translated: false
type: note
---

Question: How can I check MLflow results for a NanoChat training run like the one in the command, similar to how you can view runs in Weights & Biases?

Answer:

MLflow works differently from W&B — it’s not automatically a hosted web dashboard unless you run the MLflow server. Here’s how you can check your run:

---

### 1. Check the default MLflow location

By default, MLflow logs runs locally under the `mlruns` directory in your current working directory (`/root/nanochat/mlruns` in your case). You can explore it:

```bash
cd /root/nanochat/mlruns
ls
```

You’ll see directories for experiments (`0`, `1`, …), each containing runs with UUID-like names. Inside each run folder, you’ll find:

* `meta.yaml` → basic metadata
* `params/` → logged parameters
* `metrics/` → logged metrics
* `artifacts/` → saved models, outputs

---

### 2. Run the MLflow UI locally

MLflow has a built-in web UI. To view your experiments in a browser:

```bash
cd /root/nanochat
mlflow ui
```

By default, it will start at [http://127.0.0.1:5000](http://127.0.0.1:5000). If you are running this on a remote server, you may need to port-forward:

```bash
ssh -L 5000:127.0.0.1:5000 user@remote-server
```

Then open `http://127.0.0.1:5000` in your local browser.

---

### 3. Check the run programmatically

You can also inspect metrics and parameters using MLflow’s Python API:

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

### 4. Tips for NanoChat integration

* Make sure `--tracker=mlflow` in your command actually points to the MLflow backend you want (default is local `mlruns`).
* If you want a more W&B-like online dashboard, you can also set up MLflow to log to a remote server or cloud storage.

---

In short: **MLflow is mainly local unless you start its web UI**, unlike W&B which is cloud-hosted by default.

You can essentially do `mlflow ui` in `/root/nanochat` and open the web page to inspect metrics, parameters, and artifacts.

---

If you want, I can give you a **one-liner to open MLflow UI directly showing just your `test-mi300x` run**, so you don’t have to browse all experiments.

Do you want me to do that?
