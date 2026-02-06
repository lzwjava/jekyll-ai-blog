---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Kafka CLI 工具快速指南
translated: true
type: note
---

Kafka 提供了一些命令行工具用于管理和与集群交互。这是一份关于主要工具及其选项的全面指南。

## Core Tools

### kafka-topics.sh
管理 topic 的创建、删除和配置。

**常见操作：**

创建一个 topic：
```bash
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create \
  --topic my-topic \
  --partitions 3 \
  --replication-factor 2 \
  --config retention.ms=86400000
```

列出所有 topic：
```bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

查看 topic 详情：
```bash
kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe \
  --topic my-topic
```

删除一个 topic：
```bash
kafka-topics.sh --bootstrap-server localhost:9092 \
  --delete \
  --topic my-topic
```

修改 partitions 数量：
```bash
kafka-topics.sh --bootstrap-server localhost:9092 \
  --alter \
  --topic my-topic \
  --partitions 5
```

**关键选项：**
- `--bootstrap-server` - Kafka broker 地址（取代了已弃用的 --zookeeper）
- `--topic` - Topic 名称
- `--partitions` - Partition 数量
- `--replication-factor` - 副本系数
- `--config` - Topic 级别的配置（可以指定多次）
- `--if-not-exists` - 仅在 topic 不存在时创建
- `--if-exists` - 仅在 topic 存在时删除/修改

### kafka-console-producer.sh
从命令行发送消息。

**基本用法：**
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic my-topic
```

携带 key-value 对：
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic my-topic \
  --property "parse.key=true" \
  --property "key.separator=:"
```

从文件输入：
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic my-topic < input.txt
```

**关键选项：**
- `--property` - Producer 属性（compression.type，acks 等）
- `--producer-property` - 设置 producer 配置的另一种方式
- `--compression-codec` - 压缩类型（none，gzip，snappy，lz4，zstd）
- `--sync` - 同步发送（等待确认）
- `--timeout` - 消息超时时间（毫秒）

### kafka-console-consumer.sh
从 topic 消费消息。

**基本用法：**
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic my-topic \
  --from-beginning
```

使用 consumer group：
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic my-topic \
  --group my-consumer-group
```

显示 key 和时间戳：
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic my-topic \
  --property print.key=true \
  --property print.timestamp=true \
  --property key.separator="-"
```

**关键选项：**
- `--from-beginning` - 从最早的 offset 开始消费
- `--group` - Consumer group ID
- `--partition` - 指定消费的 partition
- `--offset` - 起始 offset（earliest，latest，或具体数值）
- `--max-messages` - 接收 N 条消息后退出
- `--property` - Consumer 属性
- `--formatter` - 自定义消息格式化类
- `--isolation-level` - read_committed 或 read_uncommitted

### kafka-consumer-groups.sh
管理 consumer groups 和 offsets。

**列出所有 consumer group：**
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

**查看 group 详情：**
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group \
  --describe
```

**重置 offsets：**
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group \
  --topic my-topic \
  --reset-offsets \
  --to-earliest \
  --execute
```

**重置 offset 选项：**
- `--to-earliest` - 重置到开头
- `--to-latest` - 重置到末尾
- `--to-offset <offset>` - 重置到指定 offset
- `--shift-by <+/- n>` - 将当前 offset 移动 n
- `--to-datetime <datetime>` - 重置到时间戳（格式：YYYY-MM-DDTHH:mm:SS.sss）
- `--by-duration <duration>` - 按时长移动（例如：PT0H30M0S）

**删除 consumer group：**
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group \
  --delete
```

### kafka-configs.sh
管理 topic、broker 和 client 的动态配置。

**添加/修改 topic 配置：**
```bash
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --alter \
  --add-config retention.ms=172800000
```

**查看 topic 配置：**
```bash
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --describe
```

**删除配置：**
```bash
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --alter \
  --delete-config retention.ms
```

**实体类型：**
- `topics` - Topic 配置
- `brokers` - Broker 配置
- `users` - 用户配额
- `clients` - 客户端配额

### kafka-log-dirs.sh
查看日志目录信息。

```bash
kafka-log-dirs.sh --bootstrap-server localhost:9092 \
  --describe \
  --broker-list 0,1,2 \
  --topic-list my-topic
```

### kafka-reassign-partitions.sh
在 broker 之间重新分配 partition。

**生成重分配计划：**
```bash
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --topics-to-move-json-file topics.json \
  --broker-list "0,1,2" \
  --generate
```

**执行重分配：**
```bash
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --reassignment-json-file reassignment.json \
  --execute
```

**验证重分配：**
```bash
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --reassignment-json-file reassignment.json \
  --verify
```

### kafka-preferred-replica-election.sh
触发首选副本（preferred replica）的 leader 选举。

```bash
kafka-preferred-replica-election.sh --bootstrap-server localhost:9092 \
  --all-topic-partitions
```

### kafka-broker-api-versions.sh
检查 broker 支持的 API 版本。

```bash
kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

### kafka-dump-log.sh
打印日志段（log segment）内容。

```bash
kafka-dump-log.sh --files /var/kafka-logs/my-topic-0/00000000000000000000.log \
  --print-data-log
```

**选项：**
- `--print-data-log` - 打印消息内容
- `--deep-iteration` - 使用深层迭代而非浅层
- `--value-decoder-class` - 自定义 value 解码类
- `--offsets-decoder` - 解码 offset 文件

### kafka-verifiable-producer.sh / kafka-verifiable-consumer.sh
用于测试和验证，发送/接收带编号的消息。

```bash
kafka-verifiable-producer.sh --bootstrap-server localhost:9092 \
  --topic test-topic \
  --max-messages 100
```

```bash
kafka-verifiable-consumer.sh --bootstrap-server localhost:9092 \
  --topic test-topic \
  --group-id test-group
```

## Common Patterns

**检查集群健康状况：**
```bash
kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

**监控 consumer 积压（lag）：**
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group \
  --describe
```

**在 topic 之间流转消息：**
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic source-topic \
  --from-beginning | \
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic dest-topic
```

**计算 topic 中的消息数量：**
```bash
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic my-topic \
  --time -1
```

所有这些工具都位于 Kafka 安装目录的 `bin/` 目录下，并有对应的 Windows `.bat` 文件。大多数工具支持 `--help` 以获取详细的选项信息。