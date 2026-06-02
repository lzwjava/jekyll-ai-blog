---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: PromQL查询语言指南
translated: true
type: note
---

PromQL（Prometheus查询语言）是一种函数式查询语言，用于从Prometheus中实时选择和聚合时间序列数据。它支持即时查询（在单个时间点评估）和范围查询（在时间范围内的多个步骤评估）。PromQL表达式可以返回四种数据类型之一：**即时向量**、**范围向量**、**标量**或**字符串**。

---

## 简介

PromQL使用户能够：

- 使用**即时向量选择器**选择时间序列。
- 使用**范围向量选择器**检索一段时间范围内的数据。
- 应用**运算符**（算术、比较、逻辑、聚合）。
- 使用函数如`rate()`、`sum()`、`avg()`进行分析。
- 通过**HTTP API**查询数据。

表达式在Prometheus UI中评估：

- **表格标签**：即时查询。
- **图形标签**：范围查询。

---

## 时间序列选择器

时间序列选择器定义要检索的指标和标签。

### 即时向量选择器

选择每个匹配时间序列的最新样本。

**语法**：

```
<指标名称>{<标签匹配器>}
```

**示例**：

- 所有具有指标`http_requests_total`的时间序列：

  ```
  http_requests_total
  ```

- 特定作业和组：

  ```
  http_requests_total{job="prometheus", group="canary"}
  ```

- 环境正则匹配并排除GET方法：

  ```
  http_requests_total{environment=~"staging|testing|development", method!="GET"}
  ```

- 匹配`__name__`：

  ```
  {__name__=~"job:.*"}
  ```

**标签匹配器**：

- `=` ：精确匹配
- `!=` ：不相等
- `=~` ：正则匹配（锚定）
- `!~` ：非正则匹配

> 注意：`{job=~".+"}`有效；单独的`{}`无效。

---

### 范围向量选择器

选择一段时间范围内的样本。

**语法**：

```
<即时选择器>[<持续时间>]
```

**示例**：

- `prometheus`作业的`http_requests_total`最近5分钟数据：

  ```
  http_requests_total{job="prometheus"}[5m]
  ```

> 范围是**左开右闭**：排除开始时间，包含结束时间。

---

### 偏移修饰符

将评估时间向前或向后移动。

**语法**：

```
<选择器> offset <持续时间>
```

**示例**：

- 5分钟前的`http_requests_total`值：

  ```
  http_requests_total offset 5m
  ```

- 1周前的速率：

  ```
  rate(http_requests_total[5m] offset 1w)
  ```

- 向前查看（负偏移）：

  ```
  rate(http_requests_total[5m] offset -1w)
  ```

> 必须紧跟在选择器之后。

---

### `@`修饰符

在特定时间戳评估。

**语法**：

```
<选择器> @ <时间戳>
```

**示例**：

- Unix时间戳`1609746000`时的值：

  ```
  http_requests_total @ 1609746000
  ```

- 特定时间的速率：

  ```
  rate(http_requests_total[5m] @ 1609746000)
  ```

- 使用`start()`或`end()`：

  ```
  http_requests_total @ start()
  rate(http_requests_total[5m] @ end())
  ```

> 可与`offset`结合使用。

---

## 速率和聚合

PromQL支持**速率**和**聚合**运算符，用于计算随时间或跨序列的指标。

### 速率函数

计算每秒平均增长率。

**示例**：

```
rate(http_requests_total[5m])
```

> 用于**范围向量**。

---

### 聚合运算符

应用于即时向量以合并时间序列。

**示例**：

- 所有`http_requests_total`的总和：

  ```
  sum(http_requests_total)
  ```

- 每个实例的平均值：

  ```
  avg by (instance)(http_requests_total)
  ```

- 每个作业的计数：

  ```
  count by (job)(http_requests_total)
  ```

> 聚合需要匹配的序列；使用`by`或`without`子句。

---

## 运算符

PromQL支持多种运算符类型。

### 算术运算符

| 运算符 | 描述       | 示例                     |
|--------|------------|--------------------------|
| `+`    | 加法       | `rate(a[5m]) + rate(b[5m])` |
| `-`    | 减法       | `rate(a[5m]) - rate(b[5m])` |
| `*`    | 乘法       | `http_requests_total * 60`  |
| `/`    | 除法       | `rate(a[5m]) / rate(b[5m])`|
| `%`    | 取模       | `http_requests_total % 100`|

> 操作数必须兼容（相同类型和形状）。

---

### 比较运算符

比较两个即时向量。

| 运算符 | 描述       | 示例                           |
|--------|------------|--------------------------------|
| `==`   | 等于       | `rate(a[5m]) == rate(b[5m])`      |
| `!=`   | 不等于     | `rate(a[5m]) != 0`                |
| `>`    | 大于       | `http_requests_total > 100`       |
| `<`    | 小于       | `http_requests_total < 10`        |
| `>=`   | 大于或等于 | `rate(a[5m]) >= 2`                |
| `<=`   | 小于或等于 | `http_requests_total <= 5`        |

> 返回布尔即时向量。

---

### 逻辑运算符

组合布尔表达式。

| 运算符 | 描述       | 示例                              |
|--------|------------|-----------------------------------|
| `and`  | 逻辑与     | `rate(a[5m]) > 1 and rate(b[5m]) > 1`|
| `or`   | 逻辑或     | `rate(a[5m]) > 1 or rate(b[5m]) > 1` |
| `unless` | 排除     | `rate(a[5m]) unless rate(b[5m]) > 0` |

> 操作数必须是相同基数的布尔向量。

---

## 函数

PromQL包含用于转换和分析的内置函数。

**常用函数**：

- `rate(v range-vector)` – 每秒速率。
- `irate(v range-vector)` – 瞬时速率（最后两个点）。
- `avg(v)` – 平均值。
- `sum(v)` – 值的总和。
- `count(v)` – 元素数量。
- `min(v)`、`max(v)` – 最小值/最大值。
- `quantile(v instant-vector, q)` – 百分位数。

**示例**：

```
quantile by (job)(0.95, http_request_duration_seconds_bucket[5m])
```

> 完整列表请参阅[Prometheus函数文档](https://prometheus.io/docs/prometheus/latest/querying/functions/)。

---

## 查询的HTTP API

PromQL查询可以通过HTTP API发送。

### 即时查询

**端点**：`/api/v1/query`

**方法**：`GET`

**参数**：

- `query`：PromQL表达式
- `time`：评估时间戳（Unix秒，可选）
- `timeout`：查询超时（例如`30s`）

**示例**：

```
GET /api/v1/query?query=http_requests_total{job="prometheus"}&time=1609746000
```

**响应**：包含`status`、`data.result`（即时向量或标量）的JSON。

---

### 范围查询

**端点**：`/api/v1/query_range`

**参数**：

- `query`：PromQL表达式
- `start`：开始时间（Unix秒）
- `end`：结束时间（Unix秒）
- `step`：分辨率步长（例如`15s`）

**示例**：

```
GET /api/v1/query_range?query=rate(http_requests_total[5m])&start=1609746000&end=1609746600&step=10s
```

**响应**：每个步骤的时间序列数据的JSON。

---

## 附加说明

- **字面量**：
  - 字符串：`"hello"`、`'world'`、`` `raw` ``
  - 浮点数：`3.14`、`-2.5e-3`、`1_000`、`0xFF`
  - 持续时间：`5m`、`1h30m`、`500ms`

- **注释**：以`#`开头

- **陈旧性**：系列在5分钟（默认）无更新后变为陈旧。

- **子查询**：在范围内运行即时查询：

  ```
  rate(http_requests_total[10m:5m])[5m]
  ```

---

本指南涵盖了PromQL的核心内容，适合初学者到中级用户。高级用法请参考[Prometheus查询基础](https://prometheus.io/docs/prometheus/latest/querying/basics/)和相关页面。
