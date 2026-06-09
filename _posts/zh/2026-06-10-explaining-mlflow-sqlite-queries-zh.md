---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解释MLflow SQLite查询
translated: true
type: note
---

问题：解释用于检查 MLflow SQLite 数据库的这些 SQL 查询。

答案：

这些查询直接使用 SQLite 读取 **MLflow 跟踪数据库** (`mlflow.db`)。

---

## 1. 计算运行时长

```sql
(r.end_time - r.start_time)/1000/60 as duration_min
FROM runs r
JOIN experiments e ON r.experiment_id = e.experiment_id
ORDER BY r.start_time;
```

### 作用

MLflow 以**Unix 纪元以来的毫秒数**存储时间戳。

示例：

```text
start_time = 1749500000000
end_time   = 1749503600000
```

差值：

```text
3600000 毫秒
```

转换为分钟：

```sql
(end_time - start_time)
/1000      -- 毫秒 → 秒
/60        -- 秒 → 分钟
```

结果：

```text
duration_min = 60
```

### 含义

显示每次训练运行的耗时。

示例：

| run          |
| ------------ |
| duration_min |
| 12.3         |
| 45.8         |
| 102.4        |

适用于：

* 训练时间比较
* 检测失败运行
* 性能基准测试

---

## 2. 显示所有参数

```sql
SELECT run_uuid, key, value
FROM params
ORDER BY run_uuid, key;
```

### MLflow 参数表

存储超参数。

示例：

| run_uuid | key        | value |
| -------- | ---------- | ----- |
| abc123   | depth      | 24    |
| abc123   | lr         | 0.001 |
| abc123   | batch_size | 32    |

含义：

```python
mlflow.log_param("depth", 24)
mlflow.log_param("lr", 0.001)
```

会在该表中创建行。

### 典型的 NanoChat 参数

你可能会看到：

```text
depth=24
window_pattern=L
device_batch_size=32
max_seq_len=2048
num_iterations=5
```

---

## 3. 显示指标历史

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

### 涉及的表格

#### metrics

存储每个记录的指标点。

示例：

| run_uuid | key  | value | step |
| -------- | ---- | ----- | ---- |
| abc123   | loss | 3.2   | 0    |
| abc123   | loss | 2.8   | 1    |
| abc123   | loss | 2.4   | 2    |

---

#### runs

包含运行元数据。

---

#### tags

存储额外信息。

示例：

```text
mlflow.runName = "depth24_batch32"
```

---

### 查询的输出

示例输出：

| run_name | key  | value | step |
| -------- | ---- | ----- | ---- |
| depth24  | loss | 3.2   | 0    |
| depth24  | loss | 2.8   | 1    |
| depth24  | loss | 2.4   | 2    |

这显示了**完整的指标历史**。

适用于绘制训练曲线。

---

## 4. 仅显示最新指标

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

### latest_metrics 表

MLflow 维护一个特殊表：

```text
latest_metrics
```

仅包含每个指标的最新值。

不再存储：

```text
loss step 0
loss step 1
loss step 2
loss step 3
```

而是保留：

```text
loss step 3
```

---

### 示例

指标历史：

| step | loss |
| ---- | ---- |
| 0    | 4.0  |
| 100  | 3.1  |
| 200  | 2.7  |
| 300  | 2.4  |

`latest_metrics` 存储：

| key  | value | step |
| ---- | ----- | ---- |
| loss | 2.4   | 300  |

---

### 为何有用

快速比较运行：

| run_name | metric | value |
| -------- | ------ | ----- |
| run1     | loss   | 2.4   |
| run2     | loss   | 2.1   |
| run3     | loss   | 1.9   |

无需扫描数百万行指标数据。

---

## MLflow 数据库结构（简化版）

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

### 关系

```text
Experiment
   └── Run
         ├── Parameters
         ├── Metrics History
         ├── Latest Metrics
         └── Tags
```

对于 NanoChat 训练运行：

* `experiments` = 训练项目
* `runs` = 单个训练尝试
* `params` = 超参数
* `metrics` = 随时间变化的 loss/perplexity 曲线
* `latest_metrics` = 最终的 loss/perplexity 值
* `tags` = 运行名称和元数据

启动 MLflow UI 后的下一步通常是：

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

然后打开：

```text
http://127.0.0.1:5000
```

可视化比较 NanoChat 运行、检查参数并查看 loss 曲线，而无需手动查询 SQLite。