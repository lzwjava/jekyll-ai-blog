---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Major Azure Outages Throughout History
translated: false
type: note
---

Microsoft Azure, launched in 2010, has experienced several significant outages over the years, often due to configuration errors, hardware failures, or external events like weather. Below is a chronological summary of the most notable ones, focusing on those with widespread impact across regions or services. This list draws from official reports, historical analyses, and incident reviews, highlighting dates, causes, affected areas, and durations where available.

| Date | Cause | Affected Regions/Services | Duration/Impact |
|------|-------|---------------------------|-----------------|
| February 29, 2012 | Leap year calculation bug in code | North America (Azure Compute) | ~8 hours; disrupted application management and services for users. |
| July 26, 2012 | Misconfigured network device | West Europe (Azure Compute) | >2 hours; partial unavailability in Europe. |
| February 22, 2013 | Expired SSL certificate | Global (Azure Storage) | Several hours; service credits issued; also hit Xbox Live, Music, and Video. |
| October 30, 2013 | Partial compute outage (throttling issue) | Worldwide (Azure Compute, management functions) | ~3-4 hours; affected file uploads and site management. |
| November 22, 2013 | Storage and network issues | North Central US (Xbox Live) | Several hours on Xbox One launch day; low customer impact but high visibility. |
| November 19, 2014 | Configuration change causing infinite loop in Blob storage | Global (20+ services, including Azure Storage) | ~6-10 hours; reduced capacity in multiple regions; impacted Xbox Live, MSN, and Visual Studio Online. |
| September 15, 2016 | Global DNS outage | Worldwide (Azure DNS) | ~2 hours; broad service disruptions. |
| March 7 & 23, 2017 | Multiple incidents (network and storage) | Global (Office 365, Skype, Xbox Live) | Up to 16+ hours each; widespread user access issues. |
| September 29, 2017 | Fire-suppression gas release during maintenance triggering shutdowns | US regions (various services) | ~7 hours; intermittent glitches. |
| September 4, 2018 | Lightning strike causing voltage spike and cooling failure | US South Central, multiple regions (40+ services) | >25 hours, some effects up to 3 days; major downtime across services. |
| January 25, 2020 | Backend dependency failure in Azure SQL Database | Global (nearly all regions, including US Gov/DoD) | ~6 hours; hit SQL DB, Application Gateway, Bastion, and Firewall. |
| April 1, 2021 | Widespread DNS issue in network infrastructure | Global (US, Europe, Asia, etc.) | ~1.5 hours; affected core network-dependent services. |
| June 1, 2022 | Issues with Azure Active Directory sign-in logs | Global (multiple regions) | ~9.5 hours; impacted AAD, Sentinel, Monitor, and Resource Manager. |
| June 29, 2022 | Unspecified backend instability | Global (dozens of regions) | ~24 hours intermittent; affected Firewall, Synapse, Backup, and more. |
| January 25, 2023 | Flawed router command causing networking disruption | Global (25+ regions, including East US, West Europe) | ~3.5 hours; latency and failures in M365 (Teams, Outlook), SharePoint, and Office 365. |
| June 9, 2023 | DDoS attack claimed by Anonymous Sudan | Global (Azure Portal and cloud services) | ~2.5 hours; portal and related services down. |
| November 13, 2024 | DNS resolution failures for Storage | Multiple (East US/2, Central US, West US/2, etc.) | ~8.5 hours; impacted Databricks and Storage Accounts. |
| December 26, 2024 | Power incident in Availability Zone | South Central US (Zone 03) | ~18 hours; hit Storage, VMs, Cosmos DB, SQL DB, and more. |
| January 9, 2025 | Networking outage | East US 2 | >48 hours; affected Databricks, Synapse, Functions, App Service, and VMs. |
| September 10, 2025 | Allocator service overload from throttling change | East US 2 (Zones 02/03) | ~10.5 hours; degraded VM operations, impacting Backup, Batch, Kubernetes, and Synapse. |
| September 26-27, 2025 | Malformed certificate value in config change | Switzerland North (multiple zones) | ~22 hours; widespread outages in API Management, App Service, Cosmos DB, VMs, and Sentinel. |
| October 9, 2025 | Azure Front Door control plane defect | Europe and Africa | ~8 hours; latency/timeouts in portals and services (up to 17% failure rate in Africa). |
| October 9, 2025 | Follow-on config removal from automation scripts | Global (management portals) | ~4 hours; access issues to Azure Portal and others post-AFD incident. |

These incidents represent a fraction of total events but the most disruptive based on scope and duration. Microsoft typically issues post-incident reviews (PIRs) for learning, and availability has improved over time, with SLAs targeting 99.99% uptime.

## References
- [A History of Microsoft Azure Outages](https://www.datacenterknowledge.com/outages/a-history-of-microsoft-azure-outages)
- [Microsoft Azure Outage History Overview](https://statusgator.com/blog/azure-outage-history/)
- [Azure Status History](https://azure.status.microsoft/en-us/status/history/)
- [Microsoft Azure Wikipedia - Outages Section](https://en.wikipedia.org/wiki/Microsoft_Azure#Outages)
