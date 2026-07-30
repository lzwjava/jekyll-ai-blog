---
audio: false
generated: true
image: false
lang: en
layout: post
title: TDengine Time-Series Database Intro
translated: false
type: note
---

Question: Intro to `taosdata/TDengine` GitHub project.

Answer:

TDengine is an open-source **time-series database (TSDB)** designed mainly for **Industrial IoT (IIoT), sensors, telemetry, connected vehicles, monitoring, and large-scale time-series analytics**. The GitHub repository is:

[TDengine GitHub repository](https://github.com/taosdata/tdengine?utm_source=chatgpt.com)

Think of TDengine as a specialized database for data like:

```
timestamp          device_id   temperature   pressure
2026-07-30 10:00   motor_001   75.2          1.3
2026-07-30 10:01   motor_001   75.4          1.4
2026-07-30 10:02   motor_002   68.1          1.1
```

Instead of normal business tables:

```
users
orders
payments
```

it optimizes for:

```
millions/billions of devices
+
continuous writes
+
time range queries
+
aggregation
```

([GitHub][1])

---

## 1. Why another database?

Traditional databases:

```
MySQL/PostgreSQL

row:
-------------------------
id | time | value | device
-------------------------
1  | 10:01| 75.2  | motor1
```

work well for transactional workloads.

But IoT creates:

```
100 million sensors

each sensor:
  every second:
      write temperature
      write vibration
      write GPS
```

Example:

```
100M sensors
×
1 event/sec
=
100M rows/sec
```

A normal OLTP database struggles.

TSDBs optimize:

* append-only writes
* timestamp ordering
* compression
* downsampling
* aggregation

Similar systems:

* InfluxData
* Timescale
* Apache IoTDB
* Prometheus

---

# 2. Architecture overview

High level:

```
                 Applications
                      |
             SQL / REST / MQTT
                      |
                TDengine Server
                      |
        +-------------+-------------+
        |                           |
   Storage Engine              Query Engine
        |                           |
   Time partition             Aggregation
   Compression                Window query
   WAL                        Downsampling
        |
     Disk files
```

The core is mostly:

* C
* C++
* some Go
* connectors in Java/Python/etc.

([GitHub][1])

---

# 3. The interesting design: Super Tables

TDengine has a unique model:

## Normal database

```
device_data

id
device_id
temperature
time
```

## TDengine

```
meters  (super table)

        tags
         |
         |
+----------------+
| temperature    |
| voltage        |
| current        |
| timestamp      |
+----------------+

        |
 -----------------
 |       |       |
dev001 dev002 dev003
```

A **super table** defines schema:

```sql
CREATE STABLE meters (
    ts TIMESTAMP,
    temperature FLOAT,
    voltage INT
)
TAGS (
    location BINARY(64),
    group_id INT
);
```

Then:

```sql
CREATE TABLE dev001
USING meters
TAGS ('factory-A',1);
```

Each device becomes a child table.

This is very optimized for IoT.

---

# 4. Storage optimization

A time-series database can exploit:

## Timestamp ordering

Usually:

```
10:00
10:01
10:02
10:03
```

not random:

```
10:03
09:20
11:00
```

So compression is much better.

Example:

Instead of storing:

```
10:00:01
10:00:02
10:00:03
```

store:

```
start timestamp
+
delta
+
delta
+
delta
```

---

## Columnar storage

Temperature:

```
75.1
75.2
75.3
75.4
```

compresses better than:

```
(device,time,temp)
(device,time,temp)
(device,time,temp)
```

---

# 5. AI features

Interesting for your AI direction:

TDengine has **TDgpt**, targeting:

* forecasting
* anomaly detection
* missing value filling
* classification

The idea:

```
sensor data
      |
      v
time-series foundation model
      |
      +---- forecast
      |
      +---- detect anomaly
      |
      +---- explain failure
```

([GitHub][1])

Industrial AI is a big area because factories generate huge telemetry streams.

---

# 6. Tech stack / repo structure

The repository:

```
TDengine/

source/
   client/
   dnode/
   vnode/
   storage/

include/

tests/

tools/

docs/
```

Build:

```bash
git clone https://github.com/taosdata/TDengine.git

cd TDengine

mkdir debug
cd debug

cmake .. -DBUILD_CONTRIB=ON

make -j$(nproc)
```

([GitHub][1])

---

# 7. How it compares to Kafka + ClickHouse + PostgreSQL

A common modern architecture:

```
Sensors
 |
 MQTT
 |
 Kafka
 |
 +-------------+
 |             |
ClickHouse   PostgreSQL
 analytics   business
```

TDengine tries to simplify:

```
Sensors
 |
 TDengine
 |
 SQL + analytics + AI
```

It combines:

* ingestion
* storage
* query
* stream processing
* analytics

([GitHub][1])

---

# 8. Why it is interesting for AI engineers

Given your LLM/infra focus, TDengine is interesting because future AI systems need **continuous data**.

Examples:

## Agent monitoring

```
100k AI agents

each emits:

latency
tokens/sec
errors
tool calls
cost
```

Store:

```
agent_id
timestamp
metric
```

TSDB fits perfectly.

---

## Robotics

```
robot arm:

camera
motor
temperature
force sensor
```

Need:

```
real-time stream
+
prediction
+
failure detection
```

---

## Training data generation

Industrial AI:

```
sensor history
       |
       v
forecast model
       |
       v
synthetic scenarios
       |
       v
RL training
```

---

# 9. My view

TDengine is a serious engineering project because it sits at the intersection of:

```
Database systems
        +
Distributed systems
        +
IoT
        +
AI agents
```

For someone learning AI infra, it is actually a good codebase to study:

* storage engine
* WAL
* indexing
* compression
* distributed consensus
* query execution

It is closer to studying ClickHouse or Apache Cassandra than building another CRUD application.

References:

* [TDengine GitHub repository](https://github.com/taosdata/tdengine?utm_source=chatgpt.com)
* [TDengine GitHub organization](https://github.com/taosdata?utm_source=chatgpt.com)

[1]: https://github.com/taosdata/tdengine?utm_source=chatgpt.com "GitHub - taosdata/TDengine: High-performance, scalable time-series database designed for Industrial IoT (IIoT) scenarios · GitHub"
