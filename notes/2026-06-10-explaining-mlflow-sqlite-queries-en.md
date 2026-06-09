---
audio: false
generated: true
image: false
lang: en
layout: post
title: Explaining MLflow SQLite Queries
translated: false
type: note
---

Question: Explain these SQL queries used to inspect an MLflow SQLite database.

Answer:

These queries are directly reading the **MLflow tracking database** (`mlflow.db`) using SQLite.

---

## 1. Calculate Run Duration

```sql
(r.end_time - r.start_time)/1000/60 as duration_min
FROM runs r
JOIN experiments e ON r.experiment_id = e.experiment_id
ORDER BY r.start_time;
```

### What it does

MLflow stores timestamps in **milliseconds since Unix epoch**.

Example:

```text
start_time = 1749500000000
end_time   = 1749503600000
```

Difference:

```text
3600000 ms
```

Convert to minutes:

```sql
(end_time - start_time)
/1000      -- ms → seconds
/60        -- seconds → minutes
```

Result:

```text
duration_min = 60
```

### Meaning

Shows how long each training run took.

Example:

| run          |
| ------------ |
| duration_min |
| 12.3         |
| 45.8         |
| 102.4        |

Useful for:

* Training time comparison
* Detecting failed runs
* Performance benchmarking

---

## 2. Show All Parameters

```sql
SELECT run_uuid, key, value
FROM params
ORDER BY run_uuid, key;
```

### MLflow params table

Stores hyperparameters.

Example:

| run_uuid | key        | value |
| -------- | ---------- | ----- |
| abc123   | depth      | 24    |
| abc123   | lr         | 0.001 |
| abc123   | batch_size | 32    |

Meaning:

```python
mlflow.log_param("depth", 24)
mlflow.log_param("lr", 0.001)
```

creates rows in this table.

### Typical NanoChat parameters

You may see:

```text
depth=24
window_pattern=L
device_batch_size=32
max_seq_len=2048
num_iterations=5
```

---

## 3. Show Metric History

```sql
SELECT
    m.run_uuid,
    substr(r.run_uuid,1,8) as run_short,
    t.value as run_name,
    m.key,
    m.value,
    m.step
FROM metrics m
JOIN runs r ON m.run_uuid = r.run_uuid
LEFT JOIN tags t
  ON t.run_uuid = r.run_uuid
 AND t.key = 'mlflow.runName'
ORDER BY r.run_uuid, m.key, m.step
LIMIT 60;
```

### Tables involved

#### metrics

Stores every logged metric point.

Example:

| run_uuid | key  | value | step |
| -------- | ---- | ----- | ---- |
| abc123   | loss | 3.2   | 0    |
| abc123   | loss | 2.8   | 1    |
| abc123   | loss | 2.4   | 2    |

---

#### runs

Contains run metadata.

---

#### tags

Stores extra information.

Example:

```text
mlflow.runName = "depth24_batch32"
```

---

### What the query produces

Example output:

| run_name | key  | value | step |
| -------- | ---- | ----- | ---- |
| depth24  | loss | 3.2   | 0    |
| depth24  | loss | 2.8   | 1    |
| depth24  | loss | 2.4   | 2    |

This shows the **full metric history**.

Useful for plotting training curves.

---

## 4. Show Latest Metrics Only

```sql
SELECT
    t.value as run_name,
    lm.key,
    lm.value as latest_value,
    lm.step
FROM latest_metrics lm
JOIN runs r ON lm.run_uuid = r.run_uuid
LEFT JOIN tags t
  ON t.run_uuid = r.run_uuid
 AND t.key = 'mlflow.runName'
ORDER BY run_name, lm.key;
```

### latest_metrics table

MLflow maintains a special table:

```text
latest_metrics
```

containing only the newest metric value for each metric.

Instead of:

```text
loss step 0
loss step 1
loss step 2
loss step 3
```

it keeps:

```text
loss step 3
```

---

### Example

Metrics history:

| step | loss |
| ---- | ---- |
| 0    | 4.0  |
| 100  | 3.1  |
| 200  | 2.7  |
| 300  | 2.4  |

`latest_metrics` stores:

| key  | value | step |
| ---- | ----- | ---- |
| loss | 2.4   | 300  |

---

### Why this is useful

Quickly compare runs:

| run_name | metric | value |
| -------- | ------ | ----- |
| run1     | loss   | 2.4   |
| run2     | loss   | 2.1   |
| run3     | loss   | 1.9   |

No need to scan millions of metric rows.

---

## MLflow Database Structure (Simplified)

```text
experiments
    │
    └── runs
            │
            ├── params
            ├── metrics
            ├── latest_metrics
            └── tags
```

### Relationship

```text
Experiment
   └── Run
         ├── Parameters
         ├── Metrics History
         ├── Latest Metrics
         └── Tags
```

For NanoChat training runs:

* `experiments` = training project
* `runs` = individual training attempts
* `params` = hyperparameters
* `metrics` = loss/perplexity curves over time
* `latest_metrics` = final loss/perplexity values
* `tags` = run names and metadata

The next step after launching the MLflow UI is usually:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Then open:

```text
http://127.0.0.1:5000
```

to compare NanoChat runs visually, inspect parameters, and view loss curves without querying SQLite manually.
