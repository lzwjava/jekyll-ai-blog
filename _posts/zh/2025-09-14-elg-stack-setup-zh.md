---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: ELG技术栈安装配置指南
translated: true
type: note
---

### ELG 技术栈概述（Elasticsearch、Logstash、Grafana）

ELG 技术栈（通常作为 ELK 技术栈的变体，使用 Grafana 替代 Kibana 进行可视化）是一套功能强大的开源工具集，用于收集、处理、存储和可视化海量数据，特别是来自应用程序、服务器和基础设施的日志数据。它支持实时监控、分析和告警功能。核心组件包括：

- **Elasticsearch**：分布式搜索和分析引擎，用于大规模数据存储、检索和分析。
- **Logstash**：数据处理管道，可从多源采集数据并进行转换后发送至 Elasticsearch。
- **Grafana**：可视化监控仪表盘工具，可连接 Elasticsearch 等数据源创建图表、图形和告警。

本指南需具备 Linux 基础知识（以 Ubuntu/Debian 为例，其他系统请调整）。完整细节请参考官方文档。安装文件需从 elastic.co 和 grafana.com 官网下载。

#### 1. 安装 Elasticsearch
Elasticsearch 负责数据存储和索引。

- **环境要求**：Java 11+（通过 `sudo apt update && sudo apt install openjdk-11-jdk` 安装）
- 下载安装：
  ```
  wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
  echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list
  sudo apt update && sudo apt install elasticsearch
  ```
- 启动并设置开机自启：`sudo systemctl start elasticsearch && sudo systemctl enable elasticsearch`
- 验证：访问 `http://localhost:9200` 应返回包含集群信息的 JSON 数据
- 基础配置（编辑 `/etc/elasticsearch/elasticsearch.yml`）：设置 `network.host: 0.0.0.0` 支持远程访问（生产环境需配置 TLS/防火墙）

#### 2. 安装 Logstash
Logstash 从数据源（如文件、系统日志）提取数据并传输至 Elasticsearch。

- 同步安装：
  ```
  sudo apt install logstash
  ```
- 启动并设置开机自启：`sudo systemctl start logstash && sudo systemctl enable logstash`
- 日志采集配置示例（`/etc/logstash/conf.d/simple.conf`）：
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
- 测试管道：`sudo /usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/simple.conf`（持久化运行需转为后台进程）
- 重载配置：`sudo systemctl restart logstash`

#### 3. 安装 Grafana
Grafana 提供可视化仪表盘展示 Elasticsearch 数据。

- 安装步骤：
  ```
  wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
  echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
  sudo apt update && sudo apt install grafana
  ```
- 启动并设置开机自启：`sudo systemctl start grafana-server && sudo systemctl enable grafana-server`
- 访问：打开 `http://localhost:3000`（默认账号 admin/admin，首次登录需修改密码）
- 连接 Elasticsearch：
  1. 进入 Configuration > Data Sources > Add data source
  2. 选择 "Elasticsearch"，设置 URL 为 `http://localhost:9200`，索引名称（如 `logstash-*`）和时间字段（如 `@timestamp`）
  3. 保存并测试连接

#### 构建完整 ELG 管道
1. **数据流**：Logstash 收集解析日志 → 传输至 Elasticsearch → Grafana 查询可视化
2. **典型工作流**：
   - 发送测试数据：使用 Logstash 输入插件或 `stdout` 等工具
   - Elasticsearch 索引：日志将以文档形式存储（可通过 Kibana API 或 curl 命令验证：`curl -X GET "localhost:9200/_search?pretty"`）
   - Grafana 仪表盘：创建面板（如通过 Lucene 查询 `program:kern*` 生成日志错误时序折线图）
3. **安全基础**：启用 HTTPS/TLS 传输认证（如 Elasticsearch 的 X-Pack 插件）和防火墙规则。生产环境需配置多节点集群
4. **监控措施**：启用 Elasticsearch 的 JVM 监控；Grafana 内置阈值告警功能

#### 常见问题与技巧
- **内存不足**：调整 `/etc/elasticsearch/jvm.options` 中的 JVM 堆参数（如 `-Xms1g -Xmx1g`）
- **端口冲突**：默认端口 Elasticsearch 9200/9300，Logstash 5044，Grafana 3000 - 可通过 `netstat -tulpn` 检查
- **性能优化**：轻量级数据采集建议使用 Beats（如 Filebeat）替代 Logstash
- **学习资源**：Elastic 官方指南（elastic.co/guide）、Grafana 文档（grafana.com/docs）。实践推荐 Docker 方案：在 GitHub 搜索 "ELG stack Docker Compose"

如需定制配置或排查特定错误，请提供更多细节。本文仅作入门指引，ELG 技术在日志分析、物联网数据和应用监控领域表现卓越。
