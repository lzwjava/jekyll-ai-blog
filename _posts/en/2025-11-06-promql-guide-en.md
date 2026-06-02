---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: PromQL Query Language Guide
translated: false
type: note
---

PromQL (Prometheus Query Language) is a functional query language used to select and aggregate time series data in real time from Prometheus. It supports instant queries (evaluated at a single point in time) and range queries (evaluated at multiple steps over a time range). PromQL expressions can return one of four data types: **instant vector**, **range vector**, **scalar**, or **string**.

---

## Introduction

PromQL enables users to:

- Select time series using **instant vector selectors**.
- Retrieve data over a time range using **range vector selectors**.
- Apply **operators** (arithmetic, comparison, logical, aggregation).
- Use **functions** like `rate()`, `sum()`, `avg()` for analysis.
- Query data via the **HTTP API**.

Expressions are evaluated in the Prometheus UI:

- **Table tab**: Instant queries.
- **Graph tab**: Range queries.

---

## Time Series Selectors

Time series selectors define which metrics and labels to retrieve.

### Instant Vector Selectors

Selects the most recent sample for each matching time series.

**Syntax**:

```
<metric_name>{<label_matchers>}
```

**Examples**:

- All time series with metric `http_requests_total`:

  ```
  http_requests_total
  ```

- Specific job and group:

  ```
  http_requests_total{job="prometheus", group="canary"}
  ```

- Regex match on environment and exclude GET method:

  ```
  http_requests_total{environment=~"staging|testing|development", method!="GET"}
  ```

- Match on `__name__`:

  ```
  {__name__=~"job:.*"}
  ```

**Label Matchers**:

- `=` : exact match
- `!=` : not equal
- `=~` : regex match (anchored)
- `!~` : no regex match

> Note: `{job=~".+"}` is valid; `{}` alone is invalid.

---

### Range Vector Selectors

Selects a range of samples over time.

**Syntax**:

```
<instant_selector>[<duration>]
```

**Example**:

- Last 5 minutes of `http_requests_total` for `prometheus` job:

  ```
  http_requests_total{job="prometheus"}[5m]
  ```

> The range is **left-open, right-closed**: excludes start time, includes end.

---

### Offset Modifier

Shifts evaluation time forward or backward.

**Syntax**:

```
<selector> offset <duration>
```

**Examples**:

- Value of `http_requests_total` 5 minutes ago:

  ```
  http_requests_total offset 5m
  ```

- Rate from 1 week ago:

  ```
  rate(http_requests_total[5m] offset 1w)
  ```

- Look ahead (negative offset):

  ```
  rate(http_requests_total[5m] offset -1w)
  ```

> Must follow selector immediately.

---

### `@` Modifier

Evaluates at a specific timestamp.

**Syntax**:

```
<selector> @ <timestamp>
```

**Examples**:

- Value at Unix timestamp `1609746000`:

  ```
  http_requests_total @ 1609746000
  ```

- Rate at specific time:

  ```
  rate(http_requests_total[5m] @ 1609746000)
  ```

- Use `start()` or `end()`:

  ```
  http_requests_total @ start()
  rate(http_requests_total[5m] @ end())
  ```

> Can be combined with `offset`.

---

## Rate and Aggregations

PromQL supports **rate** and **aggregation** operators to compute metrics over time or across series.

### Rate Function

Calculates per-second average rate of increase.

**Example**:

```
rate(http_requests_total[5m])
```

> Used on **range vectors**.

---

### Aggregation Operators

Apply to instant vectors to combine time series.

**Examples**:

- Sum of all `http_requests_total`:

  ```
  sum(http_requests_total)
  ```

- Average per instance:

  ```
  avg by (instance)(http_requests_total)
  ```

- Count per job:

  ```
  count by (job)(http_requests_total)
  ```

> Aggregation requires matching series; use `by` or `without` clauses.

---

## Operators

PromQL supports several operator types.

### Arithmetic Operators

| Operator | Description        | Example                     |
|----------|--------------------|-----------------------------|
| `+`      | Addition           | `rate(a[5m]) + rate(b[5m])` |
| `-`      | Subtraction        | `rate(a[5m]) - rate(b[5m])` |
| `*`      | Multiplication     | `http_requests_total * 60`  |
| `/`      | Division           | `rate(a[5m]) / rate(b[5m])`|
| `%`      | Modulo             | `http_requests_total % 100`|

> Operands must be compatible (same type and shape).

---

### Comparison Operators

Compare two instant vectors.

| Operator | Description        | Example                           |
|----------|--------------------|-----------------------------------|
| `==`     | Equal              | `rate(a[5m]) == rate(b[5m])`      |
| `!=`     | Not equal          | `rate(a[5m]) != 0`                |
| `>`      | Greater than       | `http_requests_total > 100`       |
| `<`      | Less than          | `http_requests_total < 10`        |
| `>=`     | Greater or equal   | `rate(a[5m]) >= 2`                |
| `<=`     | Less or equal      | `http_requests_total <= 5`        |

> Returns boolean instant vector.

---

### Logical Operators

Combine boolean expressions.

| Operator | Description        | Example                              |
|----------|--------------------|--------------------------------------|
| `and`    | Logical AND        | `rate(a[5m]) > 1 and rate(b[5m]) > 1`|
| `or`     | Logical OR         | `rate(a[5m]) > 1 or rate(b[5m]) > 1` |
| `unless` | Except             | `rate(a[5m]) unless rate(b[5m]) > 0` |

> Operands must be boolean vectors of same cardinality.

---

## Functions

PromQL includes built-in functions for transformation and analysis.

**Common Functions**:

- `rate(v range-vector)` – per-second rate.
- `irate(v range-vector)` – instantaneous rate (last two points).
- `avg(v)` – average value.
- `sum(v)` – sum of values.
- `count(v)` – number of elements.
- `min(v)`, `max(v)` – minimum/maximum.
- `quantile(v instant-vector, q)` – percentile.

**Example**:

```
quantile by (job)(0.95, http_request_duration_seconds_bucket[5m])
```

> See [Prometheus Functions Documentation](https://prometheus.io/docs/prometheus/latest/querying/functions/) for full list.

---

## HTTP API for Querying

PromQL queries can be sent via HTTP API.

### Instant Queries

**Endpoint**: `/api/v1/query`

**Method**: `GET`

**Parameters**:

- `query`: PromQL expression
- `time`: evaluation timestamp (Unix seconds, optional)
- `timeout`: query timeout (e.g., `30s`)

**Example**:

```
GET /api/v1/query?query=http_requests_total{job="prometheus"}&time=1609746000
```

**Response**: JSON with `status`, `data.result` (instant vector or scalar).

---

### Range Queries

**Endpoint**: `/api/v1/query_range`

**Parameters**:

- `query`: PromQL expression
- `start`: start time (Unix seconds)
- `end`: end time (Unix seconds)
- `step`: resolution step (e.g., `15s`)

**Example**:

```
GET /api/v1/query_range?query=rate(http_requests_total[5m])&start=1609746000&end=1609746600&step=10s
```

**Response**: JSON with time series data at each step.

---

## Additional Notes

- **Literals**:
  - Strings: `"hello"`, `'world'`, `` `raw` ``
  - Floats: `3.14`, `-2.5e-3`, `1_000`, `0xFF`
  - Durations: `5m`, `1h30m`, `500ms`

- **Comments**: Start with `#`

- **Staleness**: Series become stale after 5 minutes (default) without updates.

- **Subquery**: Run instant query over a range:

  ```
  rate(http_requests_total[10m:5m])[5m]
  ```

---

This guide covers the core of PromQL for beginners to intermediate users. For advanced usage, refer to the [Prometheus Querying Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/) and linked pages.
