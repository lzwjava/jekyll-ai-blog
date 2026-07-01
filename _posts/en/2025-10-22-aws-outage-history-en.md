---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Major AWS Outages Throughout History
translated: false
type: note
---

### Major Outages in AWS History

Amazon Web Services (AWS) has powered much of the internet since 2006, but like any large-scale infrastructure, it has faced occasional disruptions. Outages are infrequent relative to its vast operations, but major ones can ripple across dependent services, from social media to financial platforms. Below is a table summarizing key historical outages, focusing on widespread or high-impact events. These are drawn from documented incidents affecting multiple services or notable customers.

| Date | Affected Services/Regions | Cause | Impact |
| ------------------- | --------------------------- | -------------------------------- | -------- |
| February 15, 2008 | S3, EC2 (global) | Unspecified technical failure | Disrupted image storage and hosting for various websites, marking one of AWS's earliest major issues. |
| April 21, 2011 | Multiple services (US-East-1) | Extended data center failure | Took down high-profile sites like Reddit and Quora for hours, highlighting early reliability concerns. |
| February 28, 2017 | EC2, S3, RDS, and others (US-East-1) | Human error: mistyped command during debugging | Multi-hour outage affected Slack, Docker, Exora, and others; estimated losses in hundreds of millions of dollars; AWS's cloud dashboard also went down. |
| December 7, 2021 | Control plane services including EC2, RDS, Lambda (US-East-1) | Software bug in control plane during failover, leading to cascading failures | Longest outage in recent history (8+ hours); disrupted Netflix, Disney+, Capital One, and government sites; second smaller outage on Dec 15 affected similar services. |
| June 13, 2023 | EC2 and related services (multiple regions) | Unspecified regional issues | Wide-reaching downtime hit news outlets (e.g., Associated Press, Boston Globe) and transit systems (NY MTA), lasting several hours. |
| October 20, 2025 | DynamoDB endpoints, EC2 launches, and multiple services (US-East-1, with global ripple) | DNS resolution failure for DynamoDB service endpoints | Daylong disruption (starting late Oct 19 PDT, resolved by afternoon Oct 20); impacted Snapchat, Reddit, Roblox, Fortnite, banks (e.g., Lloyds), and HMRC; affected millions of users by blocking access to ~1/3 of internet-dependent apps; AWS throttled some operations for recovery. |

These incidents often stem from human error, network issues, or environmental factors, and AWS has improved resilience through redundancies like multi-region setups. The 2025 outage underscores ongoing risks of over-reliance on US-East-1, AWS's busiest region.

For more details:

- [A History of AWS Cloud and Data Center Outages](https://www.datacenterknowledge.com/outages/a-history-of-aws-cloud-and-data-center-outages)
- [The Biggest AWS Outage in History: December 7, 2021](https://aws.plainenglish.io/the-biggest-aws-outage-in-history-the-december-7-2021-us-east-1-meltdown-and-lessons-learned-2efab5a02de5)
- [What caused the AWS outage](https://www.bbc.com/news/articles/cev1en9077ro)
- [AWS Update on October 2025 Outage](https://www.aboutamazon.com/news/aws/aws-service-disruptions-outage-update)
