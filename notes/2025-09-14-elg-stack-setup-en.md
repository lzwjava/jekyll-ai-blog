---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast:free
title: ELG Stack Setup and Installation Guide
translated: false
type: note
---

### Overview of ELG Stack (Elasticsearch, Logstash, Grafana)

The ELG stack (often a variant of the ELK stack where Kibana is replaced by Grafana for visualization) is a powerful open-source suite for collecting, processing, storing, and visualizing large volumes of data, particularly logs from applications, servers, and infrastructure. It enables real-time monitoring, analytics, and alerting. Key components:

- **Elasticsearch**: A distributed search and analytics engine for storing, searching, and analyzing data at scale.
- **Logstash**: A data processing pipeline that ingests data from multiple sources, transforms it, and sends it to Elasticsearch.
- **Grafana**: A visualization and monitoring dashboard tool that connects to data sources like Elasticsearch for creating charts, graphs, and alerts.

This guide assumes basic Linux knowledge (e.g., Ubuntu/Debian; adapt for other OSes). Use official docs for full details. Installation via downloads from elastic.co and grafana.com.

#### 1. Install Elasticsearch

Elasticsearch handles data storage and indexing.

- **Prerequisites**: Java 11+ (install via `sudo apt update && sudo apt install openjdk-11-jdk`).
- Download and install:

  ```
  wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
  echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list
  sudo apt update && sudo apt install elasticsearch
  ```

- Start and enable: `sudo systemctl start elasticsearch && sudo systemctl enable elasticsearch`.
- Verify: Visit `http://localhost:9200` – should return JSON with cluster info.
- Basic config (edit `/etc/elasticsearch/elasticsearch.yml`): Set `network.host: 0.0.0.` for remote access (secure with TLS/firewall in production).

#### 2. Install Logstash

Logstash pulls data from sources (e.g., files, syslogs) and ships it to Elasticsearch.

- Install alongside Elasticsearch:

  ```
  sudo apt install logstash
  ```

- Start and enable: `sudo systemctl start logstash && sudo systemctl enable logstash`.
- Example config for ingesting logs (`/etc/logstash/conf.d/simple.conf`):

  ```
  input {
    file {
      path => "/var/log/syslog"
      start_position => "beginning"
    }
  }
  filter {
    grok {
      match => { "message" => "%{SYSLOGTIMESTAMP:timestamp} %{SYSLOGHOST:host} %{WORD:program}: %{GREEDYDATA:message}" }
    }
  }
  output {
    elasticsearch {
      hosts => ["localhost:9200"]
    }
    stdout { codec => rubydebug }
  }
  ```

- Test pipeline: `sudo /usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/simple.conf` (run in background for persistent use).
- Reload config: `sudo systemctl restart logstash`.

#### 3. Install Grafana

Grafana provides dashboards for visualizing Elasticsearch data.

- Install:

  ```
  wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
  echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
  sudo apt update && sudo apt install grafana
  ```

- Start and enable: `sudo systemctl start grafana-server && sudo systemctl enable grafana-server`.
- Access: Visit `http://localhost:3000` (default login: admin/admin; change password).
- Connect to Elasticsearch:
  1. Go to Configuration > Data Sources > Add data source.
  2. Select "Elasticsearch", set URL to `http://localhost:9200`, index name (e.g., `logstash-*`), and time field (e.g., `@timestamp`).
  3. Save and test connection.

#### Setting Up the Full ELG Pipeline

1. **Data Flow**: Logstash collects/parses logs → sends to Elasticsearch → Grafana queries and visualizes.
2. **Example Workflow**:
   - Send sample data: Use Logstash input plugins or tools like `stdout` for testing.
   - Index in Elasticsearch: Logs appear as documents (e.g., via Kibana API or direct curl: `curl -X GET "localhost:9200/_search?pretty"`).
   - Dashboard in Grafana: Create panels (e.g., line chart for log errors over time using Lucene queries like `program:kern*`).
3. **Security Basics**: Use HTTPS/TLS, authentication (e.g., X-Pack for Elasticsearch), and firewalls. For production, scale with multiple nodes/cluster.
4. **Monitoring**: Enable JVM monitoring in Elasticsearch; Grafana has built-in alerts for thresholds.

#### Common Issues and Tips

- **Out of Memory**: Increase JVM heap in `/etc/elasticsearch/jvm.options` (e.g., `-Xms1g -Xmx1g`).
- **Port Conflicts**: Default ports: Elasticsearch 9200/9300, Logstash 5044, Grafana 3000 – check `netstat -tulpn`.
- **Performance**: Use beats (e.g., Filebeat) instead of Logstash for lightweight shipping.
- **Learning Resources**: Elastic's official guides (elastic.co/guide), Grafana docs (grafana.com/docs). Practice with Docker: Search for "ELG stack Docker Compose" on GitHub.

For custom setups or troubleshooting specific errors, provide more details. This is a starting point; ELG excels in log analysis, IoT data, and app monitoring.
