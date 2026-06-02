---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Major Google Cloud Platform Outage
translated: false
type: note
---

### Overview
On June 12, 2025, Google Cloud Platform (GCP) experienced a major global outage lasting approximately 7.5 hours (from 10:51 PDT to 18:18 PDT). The incident stemmed from a bug in a newly introduced feature within Google's Service Control system, specifically related to quota policy checks. This caused an invalid automated quota update to propagate globally, leading to widespread API rejections and task overloads, particularly in high-traffic regions like us-central1 (Iowa). The outage disrupted access to numerous GCP services, Google Workspace products, and third-party applications dependent on GCP infrastructure, resulting in over 1.4 million user reports on Downdetector.

### Timeline
(All times in US/Pacific, PDT)

- **10:51 AM**: Outage begins with increased 503 errors in external API requests across multiple GCP and Google Workspace products, causing intermittent access issues.
- **11:46 AM**: Engineering teams confirm widespread service impacts; investigation underway.
- **12:09 PM**: Mitigations start; recovery in most regions except us-central1.
- **12:41 PM**: Root cause identified as invalid quota policy data; bypass implemented for quota checks.
- **1:16 PM**: Full infrastructure recovery in all regions except us-central1 and multi-region US.
- **2:00 PM**: Signs of recovery in us-central1; expected full mitigation within an hour.
- **3:16 PM**: Most GCP products recovered, but residual issues persist in Dataflow, Vertex AI, and Personalized Service Health.
- **5:06 PM**: Dataflow and Personalized Service Health resolved; Vertex AI issues ongoing with ETA of 10:00 PM.
- **6:27 PM**: Vertex AI fully recovered across all regions.
- **6:18 PM**: Incident officially ends with full service restoration.

The primary mitigation took about 3 hours, but residual backlogs and errors extended the total impact to 7.5 hours.

### Root Cause
The outage was triggered by a flaw in the Service Control feature, which manages API quotas and policies. An automated system inserted an invalid quota policy containing blank or null fields into the database. Due to global replication (designed for near-instant consistency), this corrupted data spread worldwide within seconds. When API requests hit the quota check, it resulted in null pointer exceptions and rejections (elevated 503 and 5xx errors). In large regions like us-central1, the influx of failed requests caused severe task overloads and cascading failures in dependent services. The new feature lacked sufficient validation for edge cases like blank fields, and the system did not "fail open" (allowing requests to proceed during checks).

### Affected Services
The outage impacted a broad array of Google products and external services reliant on GCP. Core GCP and Google Workspace services saw varying degrees of disruption, including API failures and UI access issues (streaming and IaaS resources were unaffected).

#### Key Google Cloud Products Affected
- **Compute & Storage**: Google Compute Engine, Cloud Storage, Persistent Disk.
- **Databases**: Cloud SQL, Cloud Spanner, Cloud Bigtable, Firestore.
- **Data & Analytics**: BigQuery, Dataflow, Dataproc, Vertex AI (including Online Prediction and Feature Store).
- **Networking & Security**: Cloud Load Balancing, Cloud NAT, Identity and Access Management (IAM), Cloud Security Command Center.
- **Developer Tools**: Cloud Build, Cloud Functions, Cloud Run, Artifact Registry.
- **AI/ML**: Vertex AI Search, Speech-to-Text, Document AI, Dialogflow.
- **Other**: Apigee, Cloud Monitoring, Cloud Logging, Resource Manager API.

#### Key Google Workspace Products Affected
- Gmail, Google Drive, Google Docs, Google Meet, Google Calendar, Google Chat.

#### Third-Party Services Impacted
Many consumer and enterprise apps hosted or partially reliant on GCP experienced downtime:
- **Spotify**: Streaming and app access disrupted for ~46,000 users.
- **Discord**: Voice chat and server connectivity issues.
- **Fitbit**: Syncing and app functionality halted.
- **Others**: OpenAI (ChatGPT), Shopify, Snapchat, Twitch, Cloudflare (cascading DNS issues), Anthropic, Replit, Microsoft 365 (partial), Etsy, Nest.

The global scale amplified the impact, as GCP powers a significant portion of the internet's backend infrastructure.

### Resolution
Google's engineering teams quickly identified the invalid policy and implemented a bypass for the quota checks, allowing API requests to proceed without validation during the crisis. This restored most regions by 12:48 PM PDT. For us-central1, targeted overload mitigations were applied, followed by manual backlog clearance in affected services like Dataflow and Vertex AI. Monitoring confirmed full recovery by 6:18 PM PDT. No data loss occurred, but some services experienced temporary delays.

### Impact
- **Scale**: Over 1.4 million Downdetector reports, highlighting real-time global disruption.
- **Economic**: Billions in potential lost productivity for businesses; Spotify alone reported user frustration during peak hours.
- **Reputation**: Underscored risks of cloud concentration, with calls for better multi-cloud strategies.

### Lessons Learned and Preventive Measures
Google issued a detailed post-mortem emphasizing resilience:
- **Architecture Changes**: Modularize Service Control to isolate failures and enable "fail-open" modes.
- **Data Validation**: Incremental propagation of global changes with pre-validation; enhanced testing for invalid inputs.
- **Deployment Safeguards**: Mandatory feature flags for critical updates; improved static analysis and error handling.
- **Monitoring & Comms**: Ensure outage detection tools remain operational independently; faster automated customer alerts.
- **Broader**: Randomized backoff in retry logic to prevent overload cascades.

These steps aim to prevent similar incidents, with ongoing audits of quota systems.

[Google Cloud Incident Report](https://status.cloud.google.com/incidents/ow5i3PPK96RduMcb1SsW)
[ThousandEyes Outage Analysis](https://www.thousandeyes.com/blog/google-cloud-outage-analysis-june-12-2025)
[Ookla Downdetector Report](https://www.ookla.com/articles/google-cloud-outage-june-2025)
[ByteByteGo Breakdown](https://blog.bytebytego.com/p/how-the-google-cloud-outage-crashed)
[Medium Root Cause Explanation](https://medium.com/@tahirbalarabe2/%EF%B8%8Fhow-a-single-google-cloud-bug-caused-global-internet-outage-on-june-12-2025-652a83ad9e68)
