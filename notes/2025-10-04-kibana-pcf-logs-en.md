---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Kibana Setup for PCF Logs
translated: false
type: note
---

It looks like "kabana" is likely a reference to **Kibana**, the open-source data visualization dashboard for Elasticsearch. In the context of **Pivotal Cloud Foundry (PCF)** (now rebranded as VMware Tanzu Application Service), Kibana is commonly used for searching, visualizing, and analyzing logs through the platform's logging system (Loggregator). PCF doesn't natively run Kibana standalone but integrates it via the **Log Search** tile/service, which stores logs in Elasticsearch and exposes Kibana for querying.

If this isn't what you meant, feel free to clarify! Below, I'll explain how to set up and use Kibana with PCF logs. This assumes you're an admin with access to PCF Ops Manager and have a running PCF deployment (version 2.0+). Note that PCF logging has evolved; check your version's documentation for specifics.

### Prerequisites

- **PCF Version**: Log Search (with Kibana) is available in PCF 2.2+. Earlier versions used a separate "ELK" (Elasticsearch, Logstash, Kibana) tile.
- **Tiles/Services**: Ensure you have the **Elastic Runtime** tile (for Loggregator) and the **Log Search** tile installed via Pivotal Network (now Broadcom Support Portal).
- **Access**: Admin privileges in Ops Manager and the PCF CLI (cf command-line tool).
- **Resources**: Allocate sufficient resources (e.g., 4-8 GB RAM for Log Search, depending on log volume).

### Step 1: Install and Configure Log Search Tile in Ops Manager

The Log Search tile forwards PCF logs (from apps, platforms, and system components) to Elasticsearch, making them searchable via Kibana.

1. **Download and Import the Tile**:
   - Log in to the Broadcom Support Portal (formerly Pivotal Network).
   - Download the **Log Search for PCF** tile (e.g., version matching your PCF release).
   - In Ops Manager (web UI), go to **Catalog** > **Import a Product** and upload the tile.

2. **Configure the Tile**:
   - In Ops Manager, go to the **Elastic Runtime** tile > **Loggregator** tab:
     - Enable **Loggregator forwarding to external systems** (e.g., set up syslog or HTTP forwarding if needed, but for Log Search, it's internal).
     - Set **Loggregator log retention** to a value like 5-30 days.
   - Go to the **Log Search** tile:
     - **Assign Availability Zones**: Select at least one AZ for high availability.
     - **Elasticsearch Configuration**:
       - Set instance count (start with 3 for production).
       - Configure storage (e.g., 100 GB persistent disks).
       - Enable security (e.g., TLS for Elasticsearch).
     - **Kibana Configuration**:
       - Enable Kibana (it's bundled).
       - Set admin credentials (username/password).
     - **Loggregator Integration**:
       - Set the maximum log lines per second (e.g., 1000-5000 based on your load).
       - Define index patterns (e.g., retain logs for 7-30 days).
     - **Networking**: Expose Kibana via a route (e.g., `kibana.YOUR-PCF-DOMAIN.com`).
   - Click **Apply Changes** to deploy. This may take 30-60 minutes.

3. **Verify Deployment**:
   - Run `cf tiles` or check Ops Manager for success.
   - SSH into a Log Search VM (using BOSH CLI: `bosh ssh log-search/0`) and confirm Elasticsearch is running (`curl localhost:9200`).

### Step 2: Access Kibana

Once deployed:

1. **Via PCF Apps Manager (GUI)**:
   - Log in to Apps Manager (e.g., `https://apps.YOUR-PCF-DOMAIN.com`).
   - Search for "Log Search" service instance (it auto-creates one).
   - Click the service instance > **Logs** tab. This opens an embedded Kibana view for quick log searches.

2. **Direct Access to Kibana**:
   - Navigate to the Kibana URL configured in the tile (e.g., `https://kibana.YOUR-PCF-DOMAIN.com`).
   - Log in with the admin credentials you set.
   - If using a custom domain, ensure DNS is pointed correctly and routes are registered (`cf routes` to verify).

3. **CLI Access (Optional)**:
   - Use `cf logs APP-NAME` for basic logs, but for advanced querying, use the Kibana UI or API.
   - Bind Log Search to your apps: `cf create-service log-search standard my-log-search` then `cf bind-service APP-NAME my-log-search`.

### Step 3: Using Kibana for PCF Logs

Kibana provides a web-based interface to query, filter, and visualize logs from PCF components (e.g., app logs, Diego cells, Gorouter, etc.).

1. **Basic Navigation**:
   - **Discover Tab**: Search logs using Lucene query syntax.
     - Example: Search for errors in a specific app: `source_id:APP:your-app-name AND json.message:ERROR`.
     - Fields available: `timestamp`, `source_id` (e.g., `APP:your-app`, `RTR:router`), `message`, `deployment`, etc.
   - **Visualize Tab**: Create dashboards for charts (e.g., log volume over time, error rates).
     - Sample visualization: Bar chart of logs by source_id.
   - **Dashboard Tab**: Save and share pre-built dashboards (Log Search includes defaults for PCF logs).

2. **Common Queries and Tips**:
   - **Filter by App**: `source_id:APP:your-app-name` (replace with actual app GUID or name).
   - **Filter by Time**: Use the time picker (e.g., last 24 hours).
   - **System Logs**: `source_id:DEA` (for Diego cells) or `source_id:LOGGREGATOR`.
   - **Export Logs**: Download as CSV/JSON from Discover.
   - **Advanced**: Use Kibana's Dev Tools (console) to query Elasticsearch directly, e.g.:

     ```
     GET /logstash-*/_search
     {
       "query": { "match": { "message": "error" } },
       "sort": [ { "timestamp": { "order": "desc" } } ]
     }
     ```

   - **Retention and Indexing**: Logs are indexed by day (e.g., `logstash-YYYY.MM.DD`). Configure rollover in the tile to manage storage.

3. **Troubleshooting Logs**:
   - **No Logs Appearing?** Check forwarding rules in Loggregator (Ops Manager > Elastic Runtime > Loggregator). Ensure apps are emitting logs (e.g., via `console.log` in Node.js).
   - **Performance Issues?** Scale up Elasticsearch instances or tune log rate limits.
   - **Security**: Enable UAA integration in Log Search for SSO login to Kibana.
   - **Errors**: Check PCF logs with `cf logs log-search` or Ops Manager errand logs.

### Additional Resources

- **Official Docs**: VMware Tanzu docs on [Log Search](https://docs.vmware.com/en/VMware-Tanzu-Application-Service/10.0/tas/GUID-log-search-index.html) (search for your version).
- **CLI Tools**: Install `uaac` for UAA auth if needed, or use `cf curl` for API access.
- **Alternatives**: For simpler needs, use PCF's built-in **Log Cache** (cf CLI: `cf tail APP-NAME`) or integrate with external tools like Splunk via syslog forwarding.
- **Upgrades**: If you're on legacy PCF, migrate to the ELK tile or contact Broadcom support.

If you provide more details (e.g., your PCF version, error messages, or specific use case), I can refine this further!
