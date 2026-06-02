---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Major Google Cloud Platform Outages
translated: false
type: note
---

### Major Outages in Google Cloud Platform (GCP) History

Google Cloud Platform has experienced several significant outages since its early days, often due to software bugs, hardware failures, environmental factors, or capacity issues. Below is a table summarizing some of the most notable ones, selected for their scale, duration, or widespread impact. These are drawn from historical records up to mid-2025.

| Date | Cause | Impact |
|------|--------|--------|
| December 14, 2020 | Accidental reduction in capacity on the central user ID management system, affecting OAuth-based authentication. | Global outage lasting ~90 minutes; disrupted access to Gmail, YouTube, Google Drive, GCP services, and apps like Pokémon GO for millions of users worldwide. |
| July 2022 | Extreme heatwave (over 40°C) in London causing cooling system failures in the europe-west2-a zone. | Regional disruptions for ~24 hours; affected Cloud Storage, BigQuery, Compute Engine, GKE, and other services, forcing failovers to other regions. |
| August 8, 2022 | Electrical incident leading to a fire at the Council Bluffs, Iowa data center (unrelated to concurrent search/maps issues). | Localized fire response; global latency in Cloud Logging service for days, impacting monitoring and debugging for GCP users. |
| April 28, 2023 | Water intrusion and fire at a Paris data center, triggering multi-cluster failures in europe-west9-a. | Widespread disruptions across Europe, Asia, Americas; hit VPC, Load Balancing, BigQuery, and networking services for hours to days. |
| August 7-8, 2024 | Failures in Cloud TPU service activation during API enablement for Vertex AI. | Global outage for ~14 hours; blocked machine learning model uploads and training in Vertex AI across all major regions. |
| October 23, 2024 | Power failure and electrical arc in europe-west3-c zone (Frankfurt), degrading cooling infrastructure. | Half-day regional outage (~8 hours); partial shutdown of infrastructure, with traffic diversion to other zones. |
| January 7-8, 2025 | Interconnected issues including SAML authentication failures in Apigee, HTTP errors in Vertex Gemini APIs, and publishing blocks in Pub/Sub. | Multi-hour disruptions over 18+ hours; affected API management, AI inference, and real-time messaging across regions. |
| June 12, 2025 | Bug in a new Service Control feature (quota policy checks) causing task overloads in large regions like us-central1. | Global outage lasting ~7 hours; knocked out Spotify, Discord, Fitbit, and many GCP-dependent services, with over 1.4 million reports. |

These incidents highlight GCP's growth pains, from early App Engine issues in the late 2000s to more recent systemic failures. Google typically issues post-mortems and remediation plans, such as modularizing components to "fail open." For the latest status, check [Google Cloud Service Health](https://status.cloud.google.com/).

[A History of Google Cloud and Data Center Outages](https://www.datacenterknowledge.com/outages/a-history-of-google-cloud-and-data-center-outages)
[Google services outages - Wikipedia](https://en.wikipedia.org/wiki/Google_services_outages)
[Google Cloud Outage History | StatusGator](https://statusgator.com/blog/google-cloud-outage-history/)
[The 10 Biggest Cloud Outages Of 2025 (So Far) - CRN](https://www.crn.com/news/cloud/2025/the-10-biggest-cloud-outages-of-2025-so-far)
[Google Cloud Outage Analysis: June 12, 2025 - ThousandEyes](https://www.thousandeyes.com/blog/google-cloud-outage-analysis-june-12-2025)
