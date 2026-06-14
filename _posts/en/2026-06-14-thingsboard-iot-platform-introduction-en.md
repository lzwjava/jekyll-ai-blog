---
audio: false
generated: true
image: false
lang: en
layout: post
title: ThingsBoard IoT Platform Introduction
translated: false
type: note
---

**Question:** What is ThingsBoard (thingsboard.io)? Give a comprehensive introduction.

**Answer:**

## ThingsBoard — Comprehensive Introduction

### What it is

ThingsBoard is an open-source IoT platform for device management, data collection, processing, and visualization. Think of it as the "backend + dashboard" layer that sits between your physical hardware (sensors, actuators, edge devices) and your application layer. You don't need to build pub/sub infrastructure, time-series storage, or dashboards from scratch — ThingsBoard does all of that.

It's used in production by Bosch, Intel, Engie, T-Mobile, Schwarz Group, and others.

---

### Core Architecture

ThingsBoard is built around 4 pillars:

**1. Device Connectivity (Transport Layer)**

Devices connect over:
- **MQTT** (primary — most IoT devices)
- **CoAP** (low-power constrained devices)
- **HTTP/HTTPS** (REST-style telemetry posting)
- **LwM2M** (OMA standard for constrained devices)
- **AMQP, Kafka** (for enterprise integrations)

Each device authenticates via tokens, X.509 certs, or basic auth. The gateway product lets you bridge legacy protocols (Modbus, BACnet, OPC-UA, CAN bus) into the ThingsBoard world.

**2. Data Model (Entities)**

ThingsBoard has a rich entity model:

```
Tenant
  └── Customer
        └── Device / Asset
              ├── Attributes (server-side, client-side, shared)
              ├── Telemetry (time-series key-value)
              ├── Alarms
              └── Relations (edges between entities)
```

- **Telemetry**: time-series data (e.g. `{"temperature": 23.4}`)
- **Attributes**: static or semi-static metadata (device config, location)
- **Relations**: build a digital twin graph — a building has floors, floors have rooms, rooms have devices

**3. Rule Engine (Processing Layer)**

This is the brain. You define data processing rule chains. Transform and normalize device data. Raise alarms on incoming telemetry events, attribute updates, device inactivity, and user actions.

Rule chains are DAGs built in a drag-and-drop editor. Node types include:

```
[Message Type Switch] → [Filter: temperature > 80] → [Create Alarm]
                                                   → [Send Email]
                                                   → [REST API Call]
                                                   → [Save to DB]
```

Rule nodes cover: JS/MVEL transformations, Kafka/RabbitMQ/SQS producers, HTTP/REST calls, alarm creation, attribute enrichment, deduplication, and more.

**4. Visualization (Dashboard Layer)**

More than 600 customizable widgets allow you to build end-user custom dashboards for most IoT use-cases. The widget library covers time-series charts, gauges, maps (Leaflet/Google Maps/OpenStreet), tables, SCADA symbols, HTML/JS custom widgets, and control widgets (sliders, buttons for RPC).

Dashboards are multi-tenant — you can expose a read-only dashboard to a specific customer with their device scope only.

---

### Product Lineup

| Product | What it is |
|---|---|
| **Community Edition (CE)** | Open-source, Apache 2.0, self-hosted |
| **Professional Edition (PE)** | Adds: advanced integrations, white-labeling, edge computing, scheduler, groups/roles |
| **ThingsBoard Cloud** | Managed SaaS (PE features, hosted by them) |
| **ThingsBoard Edge** | Runs on-premise at the edge, syncs to cloud TB instance |
| **IoT Gateway** | Agent that connects legacy protocols to ThingsBoard |
| **TBMQ** | Standalone scalable MQTT broker (Kafka-backed) |
| **Trendz Analytics** | ML-based analytics and prediction addon |

---

### Scalability Model

ThingsBoard supports microservices architecture. Amount of supported server-side requests and devices increase linearly as new ThingsBoard servers are added in clustering mode. No downtime, server restarts, or application errors.

Under the hood (PE/microservices mode):
- **Kafka** as the message bus between services
- **Cassandra** or **PostgreSQL+TimescaleDB** for time-series storage
- **Redis** for cache/sessions
- Services: `tb-core`, `tb-rule-engine`, `tb-transport` (MQTT/HTTP/CoAP), `tb-web-ui` — each independently scalable

In CE single-node mode it runs as a monolith on a single JVM, which is perfectly fine for small deployments.

---

### Multi-Tenancy

ThingsBoard supports multi-tenant installations out-of-the-box. A single tenant may have multiple tenant administrators and millions of devices and customers.

This makes it a platform-of-platforms — a company can build a white-label IoT product on top of ThingsBoard, each of their enterprise customers gets a tenant, and each enterprise customer can have sub-customers.

---

### Use Cases It's Deployed For

- Smart energy / metering (electricity, water, gas)
- Fleet tracking (GPS telemetry, geofencing)
- Smart agriculture (soil moisture, irrigation control)
- Environment monitoring (AQI, temperature/humidity)
- SCADA (industrial process control — oil/gas, power grids)
- Smart buildings / offices (HVAC, occupancy)
- Healthcare (assisted living sensor monitoring)

---

### Tech Stack

- **Backend**: Java (Spring Boot), Netty (for high-throughput MQTT), Akka/actors for rule engine
- **Frontend**: Angular
- **Storage**: PostgreSQL (attributes/entities), Cassandra or TimescaleDB (telemetry)
- **Messaging**: Kafka (in cluster mode), in-process queue (single node)
- **Deployment**: Docker, Kubernetes Helm charts, AWS/GCP/Azure marketplace images

---

### Quick Start (Docker, single-node CE)

```bash
# Pull and run ThingsBoard CE
docker run -it -p 9090:9090 -p 1883:1883 -p 7070:7070 -p 5683-5688:5683-5688/udp \
  --name mytb --restart always \
  thingsboard/tb-postgres

# Default credentials:
# Tenant: tenant@thingsboard.org / tenant
# Admin: sysadmin@thingsboard.org / sysadmin
```

Then publish telemetry via MQTT:
```bash
# Replace <ACCESS_TOKEN> with your device token
mosquitto_pub -h localhost -p 1883 \
  -t "v1/devices/me/telemetry" \
  -u "<ACCESS_TOKEN>" \
  -m '{"temperature": 25.3, "humidity": 60}'
```

Or via HTTP:
```bash
curl -v -X POST http://localhost:8080/api/v1/<ACCESS_TOKEN>/telemetry \
  --header 'Content-Type: application/json' \
  --data-raw '{"temperature": 25.3}'
```

---

### Where It Fits in the IoT Stack

```
[Physical Devices / Sensors]
        │  MQTT / CoAP / HTTP / BACnet / Modbus
        ▼
[ThingsBoard IoT Gateway]  ← bridges legacy protocols
        │
        ▼
[ThingsBoard Platform]
  ├── Transport (MQTT broker, HTTP adapter)
  ├── Rule Engine (Kafka-backed processing)
  ├── Device Registry + Digital Twins
  ├── Time-Series DB (Cassandra/TimescaleDB)
  └── Dashboard / REST API / WebSocket
        │
        ▼
[Your App / Mobile / 3rd-party: Grafana, Kafka consumers, webhooks]
```

---

### Relevance to Your Work

Given your AI + backend engineering background:

- **Rule Engine + AI**: The rule engine can call external REST APIs, so you can wire device telemetry → LLM-based anomaly detection → alarm. The new "AI Solution Creator" they just launched (June 2026) generates working IoT prototypes in 10 minutes using AI — worth watching.
- **TBMQ**: Their standalone MQTT broker is Kafka-backed and interesting from a distributed systems perspective — similar design choices to Pulsar.
- **ThingsBoard Edge**: If you're interested in edge ML (running inference close to sensors), Edge + your models is a real production pattern.
- **REST/WebSocket API**: Full programmatic control — you can drive it entirely from Python/CLI agents.

References:

- [ThingsBoard Official Site](https://thingsboard.io)
- [ThingsBoard Docs](https://thingsboard.io/docs/)
- [ThingsBoard GitHub (CE)](https://github.com/thingsboard/thingsboard)
- [Architecture / Microservices](https://thingsboard.io/docs/pe/reference/architecture/microservices/)
- [Rule Engine Docs](https://thingsboard.io/docs/pe/user-guide/rule-engine/)
