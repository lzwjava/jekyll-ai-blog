---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Kibana Log Checking Guide
translated: false
type: note
---

Kibana is an open-source data visualization and exploration tool developed by Elastic. It's a key component of the **ELK Stack** (Elasticsearch, Logstash, Kibana), which is widely used for centralized logging, monitoring, and analytics. Kibana provides a web-based interface to interact with data stored in Elasticsearch, allowing you to search, visualize, and analyze logs in real-time. It's particularly powerful for checking logs from applications, servers, or cloud services.

This guide focuses on using Kibana to inspect and query logs. We'll cover setup, basic usage, log checking workflows, and advanced tips. Assume you're working with a basic ELK setup; if you're new to ELK, start by installing Elasticsearch and Logstash first (Kibana requires Elasticsearch to function).

## 1. Prerequisites

Before using Kibana:

- **Elasticsearch**: Version 8.x or later (Kibana is tightly coupled with Elasticsearch versions). Download from [elastic.co](https://www.elastic.co/downloads/elasticsearch).
- **Java**: Elasticsearch requires JDK 11 or later.
- **System Requirements**: At least 4GB RAM for development; more for production.
- **Data Source**: Logs ingested via Logstash, Filebeat, or directly into Elasticsearch (e.g., JSON format with timestamps).
- **Network Access**: Kibana runs on port 5601 by default; ensure it's accessible.

If you don't have logs yet, use tools like Filebeat to ship sample logs (e.g., system logs) to Elasticsearch.

## 2. Installing Kibana

Kibana installation is straightforward and platform-agnostic. Download the latest version from [elastic.co/downloads/kibana](https://www.elastic.co/downloads/kibana) (match your Elasticsearch version).

### On Linux (Debian/Ubuntu)

1. Add Elastic's repository:

   ```
   wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
   sudo apt-get install apt-transport-https
   echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
   sudo apt-get update && sudo apt-get install kibana
   ```

2. Start Kibana:

   ```
   sudo systemctl start kibana
   sudo systemctl enable kibana  # For auto-start on boot
   ```

### On Windows

1. Download the ZIP archive and extract it to `C:\kibana-8.x.x-windows-x86_64`.
2. Open Command Prompt as Administrator and navigate to the extracted folder.
3. Run: `bin\kibana.bat`

### On macOS

1. Use Homebrew: `brew tap elastic/tap && brew install elastic/tap/kibana-full`.
2. Or download the TAR.GZ, extract, and run `./bin/kibana`.

For Docker: Use the official image:

```
docker run --name kibana -p 5601:5601 -e ELASTICSEARCH_HOSTS=http://elasticsearch:9200 docker.elastic.co/kibana/kibana:8.10.0
```

## 3. Basic Configuration

Edit the configuration file `kibana.yml` (located in `/etc/kibana/` on Linux, or the `config/` folder on others).

Key settings for log checking:

```yaml
# Connect to Elasticsearch (default is localhost:9200)
elasticsearch.hosts: ["http://localhost:9200"]

# Server settings
server.port: 5601
server.host: "0.0.0.0"  # Bind to all interfaces for remote access

# Security (enable for production)
# elasticsearch.username: "elastic"
# elasticsearch.password: "your_password"

# Logging
logging.verbose: true  # For debugging Kibana itself

# Index pattern (optional default)
defaultIndex: "logs-*"
```

- Restart Kibana after changes: `sudo systemctl restart kibana`.
- If using security features (X-Pack), generate certificates or use basic auth.

## 4. Starting and Accessing Kibana

- Start Elasticsearch first (e.g., `sudo systemctl start elasticsearch`).
- Start Kibana as above.
- Open a web browser and go to `http://localhost:5601` (or your server's IP:5601).
- On first login, you'll see the setup wizard. Create an admin user if prompted (default: elastic/changeme).

The interface includes apps like **Discover** (for logs), **Visualize**, **Dashboard**, **Dev Tools**, and **Management**.

## 5. Preparing Data: Index Patterns

Logs in Elasticsearch are stored in **indices** (e.g., `logs-2023-10-01`). To query them in Kibana, create an **index pattern**.

1. Go to **Stack Management** > **Index Patterns** (left sidebar, hamburger menu > Management).
2. Click **Create index pattern**.
3. Enter a pattern like `logs-*` (matches all log indices) or `filebeat-*` (for Filebeat logs).
4. Select the **Time field** (e.g., `@timestamp` for log timestamps—crucial for time-based queries).
5. Click **Create index pattern**.
   - This maps fields like `message` (log text), `host.name`, `level` (error/warn/info), etc.

Refresh fields if your logs change. Use **Discover** to preview.

## 6. Using Discover to Check Logs

The **Discover** app is your primary tool for inspecting logs. It's like a searchable log viewer.

### Basic Navigation

1. Click **Discover** in the left sidebar.
2. Select your index pattern from the dropdown (top-left).
3. Set the time range (top-right): Use quick options like "Last 15 minutes" or custom (e.g., Last 7 days). This filters logs by `@timestamp`.

### Viewing Logs

- **Hit Count**: Shows total matching logs (e.g., 1,234 hits).
- **Document Table**: Displays raw log entries as JSON or formatted text.
  - Columns: Default is `@timestamp` and `_source` (full log). Drag fields from the left sidebar (e.g., `message`, `host.name`) to add columns.
  - Expand a row (click the arrow) to see the full JSON document.
- **Histogram**: Top chart shows log volume over time. Zoom by dragging.

### Searching Logs

Use the search bar (top) for queries. Kibana uses **KQL (Kibana Query Language)** by default—simple and intuitive.

- **Basic Search**:
  - Search for a keyword: `error` (finds logs containing "error").
  - Field-specific: `host.name:webserver AND level:error` (logs from "webserver" with error level).
  - Phrases: `"user login failed"` (exact match).

- **Filters**:
  - Add from sidebar: Click a field value (e.g., `level: ERROR`) > Add filter (pins it to the query).
  - Boolean logic: `+error -info` (must have "error", exclude "info").
  - Range: For numbers/times, e.g., `bytes:>1000` (field > 1000).

- **Advanced Queries**:
  - Switch to **Lucene query syntax** (via query language dropdown) for complex needs: `message:(error OR warn) AND host.name:prod*`.
  - Use **Query DSL** in Dev Tools for Elasticsearch-native queries (e.g., POST /logs-*/_search with JSON body).

### Saving Searches

- Click **Save** (top-right) to store a search for reuse.
- Share via **Share** > CSV/URL for exports.

Example Workflow: Checking Application Logs

1. Ingest logs (e.g., via Logstash: input file > filter grok/parse > output Elasticsearch).
2. In Discover: Time range "Last 24 hours".
3. Search: `app.name:myapp AND level:ERROR`.
4. Add filters: `host.name` = specific server.
5. Inspect: Look at `message` for stack traces, correlate with `@timestamp`.

## 7. Visualizing Logs

While Discover is for raw checking, visualize for patterns.

### Create Visualizations

1. Go to **Visualize Library** > **Create new visualization**.
2. Choose type:
   - **Lens** (easy): Drag fields to buckets (e.g., X-axis: `@timestamp`, Y-axis: count of errors).
   - **Area/Line Chart**: For log volume over time (Metrics: Count, Buckets: Date Histogram on `@timestamp`).
   - **Data Table**: Tabular log summary.
   - **Pie Chart**: Breakdown by `level` (error 40%, info 60%).
3. Apply filters/searches from Discover.
4. Save and add to a **Dashboard** (Analytics > Dashboard > Create new > Add visualization).

Example: Error Rate Dashboard

- Visualize: Line chart of error logs per hour.
- Filter: Global time range.
- Embed in Dashboard for monitoring.

## 8. Advanced Features for Log Analysis

- **Alerts and Monitoring**:
  - Use **Alerts** (Stack Management > Rules) to notify on log patterns (e.g., email if "critical" appears >5 times/hour).
  - **Uptime Monitoring** or **APM** for app logs.

- **Machine Learning**:
  - Enable ML jobs (Stack Management > Machine Learning) to detect anomalies in log volumes.

- **Dev Tools**:
  - Console for raw Elasticsearch queries: e.g.,

    ```
    GET logs-*/_search
    {
      "query": { "match": { "message": "error" } },
      "sort": [ { "@timestamp": "desc" } ]
    }
    ```

  - Test index patterns or ingest data.

- **Roles and Security**:
  - In production, use **Spaces** to isolate log views (e.g., dev/prod).
  - Role-based access: Restrict users to specific indices.

- **Export/Import**:
  - Export searches/dashboards as NDJSON via **Stack Management > Saved Objects**.
  - Import logs via **Console** or Beats.

- **Performance Tips**:
  - Use **Field Analyzer** (Index Patterns > field) for custom mappings.
  - Paginate large results: Adjust hits per page (Discover settings).
  - For big data, shard indices and use ILM (Index Lifecycle Management).

## 9. Integrating with Log Sources

- **Filebeat/Logstash**: Ship logs to Elasticsearch.
  - Example Filebeat config (`filebeat.yml`):

    ```yaml
    filebeat.inputs:
    - type: log
      paths: [/var/log/*.log]
      fields:
        app: myapp
    output.elasticsearch:
      hosts: ["localhost:9200"]
      index: "logs-%{+yyyy.MM.dd}"
    ```

  - Run: `./filebeat -e`.
- **Cloud Logs**: Integrate with AWS S3, Azure, or Elastic Cloud for managed setups.

## 10. Troubleshooting Common Issues

- **No Data in Discover**:
  - Check Elasticsearch connection: `curl localhost:9200/_cat/indices`.
  - Verify index pattern matches indices (e.g., no `*` mismatch).
  - Ensure `@timestamp` is mapped as date.

- **Kibana Won't Start**:
  - Logs: Check `/var/log/kibana/kibana.log` or console output.
  - Common: Port 5601 in use, or Elasticsearch not running/secure.

- **Slow Queries**:
  - Optimize: Use keyword fields for filters, avoid wildcards on large texts.
  - Increase heap: Edit `jvm.options` for Elasticsearch (e.g., `-Xms4g -Xmx4g`).

- **Errors in Logs**:
  - 403/401: Authentication issues—enable security in `elasticsearch.yml`.
  - Version Mismatch: Ensure Kibana == Elasticsearch version.

- **Resources**:
  - Official Docs: [elastic.co/guide/en/kibana/current](https://www.elastic.co/guide/en/kibana/current/index.html).
  - Forums: Elastic Discuss or Stack Overflow.
  - Sample Data: Load via Kibana (Stack Management > Kibana > Sample Data).

This guide should get you started with Kibana for log checking. Start small: Set up a local ELK stack, ingest sample logs, and experiment in Discover. For production, consider Elastic Cloud for ease. If you have a specific setup (e.g., Docker, AWS), provide more details for tailored advice!
