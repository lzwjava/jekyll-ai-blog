---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Kafka CLI Tools Quick Guide
translated: false
type: note
---

Kafka provides several command-line tools for managing and interacting with clusters. Here's a comprehensive guide to the main tools and their options.

## Core Tools

### kafka-topics.sh
Manages topic creation, deletion, and configuration.

**Common operations:**

Creating a topic:
```bash
kafka-topics.sh --bootstrap-server localhost:9092 \
  --create \
  --topic my-topic \
  --partitions 3 \
  --replication-factor 2 \
  --config retention.ms=86400000
```

Listing topics:
```bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

Describing a topic:
```bash
kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe \
  --topic my-topic
```

Deleting a topic:
```bash
kafka-topics.sh --bootstrap-server localhost:9092 \
  --delete \
  --topic my-topic
```

Altering partitions:
```bash
kafka-topics.sh --bootstrap-server localhost:9092 \
  --alter \
  --topic my-topic \
  --partitions 5
```

**Key options:**
- `--bootstrap-server` - Kafka broker address (replaces deprecated --zookeeper)
- `--topic` - Topic name
- `--partitions` - Number of partitions
- `--replication-factor` - Replication factor
- `--config` - Topic-level configuration (can specify multiple times)
- `--if-not-exists` - Only create if topic doesn't exist
- `--if-exists` - Only delete/alter if topic exists

### kafka-console-producer.sh
Produces messages from the command line.

**Basic usage:**
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic my-topic
```

With key-value pairs:
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic my-topic \
  --property "parse.key=true" \
  --property "key.separator=:"
```

From a file:
```bash
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic my-topic < input.txt
```

**Key options:**
- `--property` - Producer properties (compression.type, acks, etc.)
- `--producer-property` - Alternative way to set producer configs
- `--compression-codec` - Compression type (none, gzip, snappy, lz4, zstd)
- `--sync` - Synchronous sending (wait for acknowledgment)
- `--timeout` - Message timeout in milliseconds

### kafka-console-consumer.sh
Consumes messages from topics.

**Basic usage:**
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic my-topic \
  --from-beginning
```

With consumer group:
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic my-topic \
  --group my-consumer-group
```

Showing keys and timestamps:
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic my-topic \
  --property print.key=true \
  --property print.timestamp=true \
  --property key.separator="-"
```

**Key options:**
- `--from-beginning` - Consume from earliest offset
- `--group` - Consumer group ID
- `--partition` - Specific partition to consume from
- `--offset` - Starting offset (earliest, latest, or numeric)
- `--max-messages` - Exit after N messages
- `--property` - Consumer properties
- `--formatter` - Custom message formatter class
- `--isolation-level` - read_committed or read_uncommitted

### kafka-consumer-groups.sh
Manages consumer groups and offsets.

**List all groups:**
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

**Describe a group:**
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group \
  --describe
```

**Reset offsets:**
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group \
  --topic my-topic \
  --reset-offsets \
  --to-earliest \
  --execute
```

**Reset offset options:**
- `--to-earliest` - Reset to beginning
- `--to-latest` - Reset to end
- `--to-offset <offset>` - Reset to specific offset
- `--shift-by <+/- n>` - Shift current offset by n
- `--to-datetime <datetime>` - Reset to timestamp (format: YYYY-MM-DDTHH:mm:SS.sss)
- `--by-duration <duration>` - Shift by duration (e.g., PT0H30M0S)

**Delete a group:**
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group \
  --delete
```

### kafka-configs.sh
Manages dynamic configurations for topics, brokers, and clients.

**Add/modify topic config:**
```bash
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --alter \
  --add-config retention.ms=172800000
```

**Describe topic configs:**
```bash
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --describe
```

**Delete config:**
```bash
kafka-configs.sh --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --alter \
  --delete-config retention.ms
```

**Entity types:**
- `topics` - Topic configurations
- `brokers` - Broker configurations
- `users` - User quotas
- `clients` - Client quotas

### kafka-log-dirs.sh
Describes log directory information.

```bash
kafka-log-dirs.sh --bootstrap-server localhost:9092 \
  --describe \
  --broker-list 0,1,2 \
  --topic-list my-topic
```

### kafka-reassign-partitions.sh
Reassigns partitions across brokers.

**Generate reassignment plan:**
```bash
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --topics-to-move-json-file topics.json \
  --broker-list "0,1,2" \
  --generate
```

**Execute reassignment:**
```bash
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --reassignment-json-file reassignment.json \
  --execute
```

**Verify reassignment:**
```bash
kafka-reassign-partitions.sh --bootstrap-server localhost:9092 \
  --reassignment-json-file reassignment.json \
  --verify
```

### kafka-preferred-replica-election.sh
Triggers preferred replica leader election.

```bash
kafka-preferred-replica-election.sh --bootstrap-server localhost:9092 \
  --all-topic-partitions
```

### kafka-broker-api-versions.sh
Checks API versions supported by brokers.

```bash
kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

### kafka-dump-log.sh
Prints log segment contents.

```bash
kafka-dump-log.sh --files /var/kafka-logs/my-topic-0/00000000000000000000.log \
  --print-data-log
```

**Options:**
- `--print-data-log` - Print message contents
- `--deep-iteration` - Use deep iteration instead of shallow
- `--value-decoder-class` - Custom decoder for values
- `--offsets-decoder` - Decode offset files

### kafka-verifiable-producer.sh / kafka-verifiable-consumer.sh
Used for testing and verification, producing/consuming numbered messages.

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

**Check cluster health:**
```bash
kafka-broker-api-versions.sh --bootstrap-server localhost:9092
```

**Monitor consumer lag:**
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group \
  --describe
```

**Stream messages between topics:**
```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic source-topic \
  --from-beginning | \
kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic dest-topic
```

**Count messages in a topic:**
```bash
kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic my-topic \
  --time -1
```

All these tools are located in the `bin/` directory of your Kafka installation and have corresponding `.bat` files for Windows. Most tools support `--help` for detailed option information.
