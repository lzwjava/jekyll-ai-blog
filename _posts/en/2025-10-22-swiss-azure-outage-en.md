---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Major Azure Outage in Switzerland North
translated: false
type: note
---

### Azure Outage in Switzerland North: September 26-27, 2025

This incident was a major platform-wide disruption in the Switzerland North region, affecting multiple availability zones. It lasted approximately 22 hours, starting at 23:54 UTC on September 26 and fully resolving by 21:59 UTC on September 27. While most services recovered by around 04:00 UTC on September 27, some residual issues required manual intervention later in the day.

#### Root Cause

The outage stemmed from a planned configuration change to certificates used for authorizing communication in the software load balancer infrastructure. One of the new certificates had a **malformed value** that wasn't caught during validation. This change followed an expedited deployment path, which unexpectedly rolled it out across multiple zones without triggering health safeguards. As a result:

- Load balancers lost connectivity to storage resources and nodes.
- Affected VMs detected prolonged disk disconnections and shut down automatically to avoid data corruption.
- This cascaded to dependent services, amplifying the impact.

#### Affected Services

The disruption hit a broad range of Azure services hosted in Switzerland North, including:

- **Core infrastructure**: Azure Storage, Azure Virtual Machines (VMs), Azure Virtual Machine Scale Sets (VMSS)
- **Databases**: Azure Cosmos DB, Azure SQL Database, Azure SQL Managed Instance, Azure Database for PostgreSQL
- **Compute and apps**: Azure App Service, Azure API Management, Azure Kubernetes Service (AKS), Azure Databricks
- **Networking and security**: Azure Application Gateway, Azure Firewall, Azure Cache for Redis
- **Analytics and monitoring**: Azure Synapse Analytics, Azure Data Factory, Azure Stream Analytics, Azure Data Explorer, Azure Log Analytics, Microsoft Sentinel
- **Other**: Azure Backup, Azure Batch, Azure Site Recovery, Azure Application Insights

Services relying on these (e.g., custom applications) were also impacted, leading to widespread unavailability or degraded performance.

#### Timeline and Mitigation

- **23:54 UTC, Sep 26**: Impact begins after the config change deploys.
- **00:08 UTC, Sep 27**: Automated monitoring detects the issue.
- **00:12 UTC, Sep 27**: Investigation starts by Azure Storage and Networking teams.
- **02:33 UTC, Sep 27**: Revert the config change.
- **03:40 UTC, Sep 27**: Certificate revert completes.
- **04:00 UTC, Sep 27**: Majority of services recover automatically; residual issues identified (e.g., certain VMs in stopped/unhealthy states due to race conditions or misinterpreted shutdown signals).
- **06:19–14:15 UTC, Sep 27**: Develop and validate recovery scripts; perform targeted restarts for affected resources like SQL Managed Instance VMs, Trusted Launch VMs, and Service Fabric clusters.
- **16:15 UTC, Sep 27**: Partial recovery for residuals.
- **21:59 UTC, Sep 27**: Full recovery confirmed after final validations.

Most resources auto-recovered post-connectivity restoration, but subsets (e.g., VMs with custom extensions) needed manual reboots to resolve startup sequence issues.

#### Lessons Learned and Improvements

Microsoft's Preliminary Incident Review highlights proactive fixes:

- Added auditing to deployment systems and removed risky expedited pipelines (completed).
- Enhanced safety measures with automated rollbacks (completed).
- Upcoming: Better monitoring for resource health (by Nov 2025) and resilient recovery processes to minimize manual work.

This event underscores the risks of config changes in shared infrastructure, but Azure's response limited data loss and enabled quick broad recovery.

[Azure Status History](https://azure.status.microsoft/en-us/status/history/)
