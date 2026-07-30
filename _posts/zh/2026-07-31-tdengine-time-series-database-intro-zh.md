---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TDengine 时序数据库简介
translated: true
type: note
---

问题：介绍 `taosdata/TDengine` GitHub 项目。

回答：

TDengine 是一个开源的**时序数据库 (TSDB)**，主要面向**工业物联网 (IIoT)、传感器、遥测、车联网、监控以及大规模时序数据分析**。其 GitHub 仓库地址为：

[TDengine GitHub 仓库](https://github.com/taosdata/tdengine?utm_source=chatgpt.com)

可以将 TDengine 视为一个专门处理如下数据的数据库：

```
timestamp          device_id   temperature   pressure
2026-07-30 10:00   motor_001   75.2          1.3
2026-07-30 10:01   motor_001   75.4          1.4
2026-07-30 10:02   motor_002   68.1          1.1
```

与普通的业务数据表不同：

```
users
orders
payments
```

它针对以下场景进行了优化：

```
数百万/数十亿的设备
+
持续写入
+
时间范围查询
+
聚合操作
```

([GitHub][1])

---

## 1. 为什么还需要另一个数据库？

传统数据库：

```
MySQL/PostgreSQL

行:
-------------------------
id | time | value | device
-------------------------
1  | 10:01| 75.2  | motor1
```

对于事务性工作负载表现良好。

但物联网带来了以下挑战：

```
1亿个传感器

每个传感器:
  每秒:
      写入温度数据
      写入振动数据
      写入GPS数据
```

示例：

```
1亿个传感器
×
每秒1个事件
=
每秒1亿行数据
```

普通的 OLTP 数据库难以应对。

时序数据库 (TSDB) 针对以下方面进行了优化：

* 仅追加写入
* 时间戳排序
* 压缩
* 降采样
* 聚合

类似的系统：

* InfluxData
* Timescale
* Apache IoTDB
* Prometheus

---

# 2. 架构概览

高层架构：

```
                 应用程序
                      |
             SQL / REST / MQTT
                      |
                TDengine Server
                      |
        +-------------+-------------+
        |                           |
   存储引擎                   查询引擎
        |                           |
   时间分区                  聚合操作
   压缩                      窗口查询
   WAL                       降采样
        |
     磁盘文件
```

核心技术栈主要为：

* C 语言
* C++ 语言
* 部分 Go 语言
* Java/Python 等语言的连接器

([GitHub][1])

---

# 3. 有趣的设计：超级表 (Super Tables)

TDengine 拥有独特的模型：

## 普通数据库：

```
device_data

id
device_id
temperature
time
```

## TDengine：

```
meters  (超级表)

        标签
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

**超级表** 定义了模式：

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

然后：

```sql
CREATE TABLE dev001
USING meters
TAGS ('factory-A',1);
```

每个设备都成为一个子表。

这种设计针对物联网进行了高度优化。

---

# 4. 存储优化

时序数据库可以利用以下特性：

## 时间戳排序

通常是：

```
10:00
10:01
10:02
10:03
```

而不是随机的：

```
10:03
09:20
11:00
```

因此压缩效率更高。

例如：

无需存储：

```
10:00:01
10:00:02
10:00:03
```

而是存储：

```
起始时间戳
+
差值
+
差值
+
差值
```

---

## 列式存储

温度数据：

```
75.1
75.2
75.3
75.4
```

比以下方式的压缩效果更好：

```
(device,time,temp)
(device,time,temp)
(device,time,temp)
```

---

# 5. AI 功能

对于您的人工智能方向来说，值得关注的是：

TDengine 包含 **TDgpt**，目标功能包括：

* 预测
* 异常检测
* 缺失值填充
* 分类

其理念如下：

```
传感器数据
      |
      v
时序基础模型
      |
      +---- 预测
      |
      +---- 检测异常
      |
      +---- 解释故障
```

([GitHub][1])

工业人工智能是一个重要领域，因为工厂会产生海量的遥测数据流。

---

# 6. 技术栈 / 仓库结构

该仓库结构如下：

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

构建方式：

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

# 7. 与 Kafka + ClickHouse + PostgreSQL 方案的对比

一种常见的现代架构是：

```
传感器
 |
 MQTT
 |
 Kafka
 |
 +-------------+
 |             |
ClickHouse   PostgreSQL
 分析        业务数据
```

TDengine 试图简化此架构：

```
传感器
 |
 TDengine
 |
 SQL + 分析 + AI
```

它整合了：

* 数据摄入
* 存储
* 查询
* 流处理
* 分析

([GitHub][1])

---

# 8. 为什么对 AI 工程师有吸引力

鉴于您专注于 LLM/基础设施领域，TDengine 之所以值得关注，是因为未来的 AI 系统需要**持续的数据流**。

示例：

## 智能体监控

```
10万个 AI 智能体

每个智能体产生：

延迟
每秒 tokens 数
错误数
工具调用次数
成本
```

存储方式：

```
agent_id
timestamp
metric
```

时序数据库 (TSDB) 非常适合。

---

## 机器人技术

```
机械臂：

摄像头
马达
温度
力传感器
```

需求：

```
实时数据流
+
预测
+
故障检测
```

---

## 训练数据生成

工业人工智能：

```
传感器历史数据
       |
       v
预测模型
       |
       v
合成场景数据
       |
       v
强化学习训练
```

---

# 9. 我的看法

TDengine 是一个严谨的工程项目，因为它处于以下领域的交汇点：

```
数据库系统
        +
分布式系统
        +
物联网
        +
AI 智能体
```

对于正在学习 AI 基础设施的人来说，它实际上是一个值得研究的好代码库：

* 存储引擎
* 预写日志 (WAL)
* 索引
* 压缩
* 分布式共识
* 查询执行

这更接近于研究 ClickHouse 或 Apache Cassandra，而不是构建另一个 CRUD 应用程序。

参考：

* [TDengine GitHub 仓库](https://github.com/taosdata/tdengine?utm_source=chatgpt.com)
* [TDengine GitHub 组织](https://github.com/taosdata?utm_source=chatgpt.com)

[1]: https://github.com/taosdata/tdengine?utm_source=chatgpt.com "GitHub - taosdata/TDengine: 高性能、可扩展的时序数据库，专为工业物联网 (IIoT) 场景设计"