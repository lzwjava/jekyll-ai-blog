---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: AWS Outage Case Analysis October 2025
translated: false
type: note
---

### AWS Outage on October 20, 2025: Detailed Case Analysis

The AWS outage on October 20, 2025, was a significant disruption originating in the US East (N. Virginia) region (us-east-1), AWS's largest and most critical data center. It began late on October 19 PDT and lasted approximately 16 hours, affecting over 140 services and cascading globally due to dependencies on this region. The incident highlighted vulnerabilities in DNS resolution, service interdependencies, and recovery processes, impacting millions of users across apps, websites, and services. Below is a breakdown based on AWS's official post-mortem and contemporaneous reports.

#### Timeline
The outage unfolded in phases, starting with detection and escalating to cascading failures before a staggered recovery. Key milestones (all times in PDT):

| Time | Event |
|------|-------|
| 11:49 PM (Oct 19) | Increased error rates and latencies detected across multiple AWS services in us-east-1. |
| 12:11 AM (Oct 20) | AWS publicly reports elevated error rates; initial user reports spike on monitoring sites like DownDetector. |
| 12:26 AM | Issue pinpointed to DNS resolution failures for DynamoDB API endpoints in us-east-1. |
| 1:26 AM | Confirmed high error rates specifically for DynamoDB APIs, including Global Tables. |
| 2:22 AM | Initial mitigations applied; early recovery signs emerge. |
| 2:24 AM | DynamoDB DNS issue resolved, triggering partial service recovery—but EC2 launch impairments and Network Load Balancer (NLB) health check failures surface. |
| 3:35 AM | DNS fully mitigated; most DynamoDB operations succeed, but EC2 launches remain impaired across Availability Zones (AZs). |
| 4:08 AM | Ongoing work on EC2 errors and Lambda polling delays for SQS Event Source Mappings. |
| 5:48 AM | Partial EC2 launch recovery in select AZs; SQS backlogs begin clearing. |
| 6:42 AM | Mitigations rolled out across AZs; AWS implements rate limiting on new EC2 instance launches to stabilize. |
| 7:14 AM | API errors and connectivity issues persist across services; user-impacting failures peak (e.g., app outages). |
| 8:04 AM | Investigation focuses on EC2 internal network. |
| 8:43 AM | Root cause for network issues identified: impairment in EC2's internal subsystem for NLB health monitoring. |
| 9:13 AM | Additional mitigations for NLB health checks. |
| 9:38 AM | NLB health checks fully recovered. |
| 10:03 AM – 12:15 PM | Progressive EC2 launch improvements; Lambda invocations and connectivity stabilize in phases across AZs. |
| 1:03 PM – 2:48 PM | Throttles reduced; backlogs processed for services like Redshift, Amazon Connect, and CloudTrail. |
| 3:01 PM | Full operational normalcy restored for all services; minor backlogs (e.g., AWS Config, Redshift) expected to clear within hours. |
| 3:53 PM | AWS declares outage resolved. |

User reports on platforms like DownDetector peaked around 6 AM PDT, with over 5,000 incidents before dropping.

#### Root Cause
The outage stemmed from a DNS resolution failure affecting DynamoDB service endpoints in us-east-1. DynamoDB, a NoSQL database service, acts as a critical "control plane" for many AWS features—handling metadata, sessions, and routing. When DNS failed to resolve these endpoints, DynamoDB APIs experienced elevated latencies and errors.

This initial issue resolved quickly, but it triggered a cascade:
- EC2 instance launches failed due to their dependency on DynamoDB for metadata storage.
- An underlying bug in EC2's internal subsystem (responsible for monitoring NLB health) exacerbated network connectivity issues, leading to broader impairments in load balancing and API calls.
- Recovery efforts involved throttling (e.g., limiting EC2 launches and Lambda invocations) to prevent overload, but retries from dependent services amplified the strain.

AWS confirmed it was not a cyberattack but an infrastructure-related glitch, possibly tied to a faulty DNS database update or backup system failure. The global ripple occurred because us-east-1 hosts key control planes for services like IAM and Lambda, even for resources in other regions.

#### Affected Services
Over 142 AWS services were impacted, primarily those reliant on DynamoDB, EC2, or us-east-1 endpoints. Core categories:

- **Database & Storage**: DynamoDB (primary), RDS, Redshift, SQS (backlogs).
- **Compute & Orchestration**: EC2 (launches), Lambda (invocations, polling), ECS, EKS, Glue.
- **Networking & Load Balancing**: Network Load Balancer (health checks), API Gateway.
- **Monitoring & Management**: CloudWatch, CloudTrail, EventBridge, IAM (updates), AWS Config.
- **Other**: Amazon Connect, Athena, and global features like DynamoDB Global Tables.

Not all services were fully down—many saw partial errors or delays—but the interconnected nature meant even minor issues propagated.

#### Impacts
The outage disrupted ~1/3 of internet-dependent applications, affecting an estimated 100+ million users worldwide. High-profile examples:
- **Social & Media**: Snapchat (login failures), Reddit (outages), Twitch (streaming issues).
- **Gaming**: Roblox (server crashes), Fortnite (matchmaking failures).
- **Finance & Payments**: Venmo, banks like Lloyds (transaction delays), HMRC (UK tax services).
- **Retail & E-commerce**: Portions of Amazon's own retail site; airline check-ins (e.g., Delta, United delays).
- **Other**: Alexa devices (voice failures), Twilio (communications glitches).

Economic estimates peg losses at $500 million+, with a 300% spike in cybersecurity scans as users panicked. It underscored the internet's centralization: us-east-1 handles ~30% of AWS traffic, making it a single point of fragility despite multi-AZ designs.

#### Resolution and Lessons Learned
AWS resolved the issue through targeted mitigations: DNS fixes, subsystem patches for EC2/NLB, and progressive throttle reductions. Post-incident, they advised:
- Retrying failed requests.
- Flushing DNS caches.
- Distributing resources across multiple AZs/regions (e.g., via Auto Scaling Groups).
- Using service quotas and caching to buffer against retries.

Broader takeaways include the need for better redundancy in control planes, AI-driven anomaly detection for faster triage, and diversified cloud strategies. AWS committed to a full root cause analysis (RCA) for customers, emphasizing that such events, while rare, reveal scaling challenges at hyperscale.

This was AWS's most disruptive us-east-1 outage since 2021, but recovery was faster than historical precedents due to automated tools.

#### References
- [AWS Health Dashboard: Service Health - Oct 20, 2025](https://health.aws.amazon.com/health/status?eventID=arn:aws:health:us-east-1::event/MULTIPLE_SERVICES/AWS_MULTIPLE_SERVICES_OPERATIONAL_ISSUE/AWS_MULTIPLE_SERVICES_OPERATIONAL_ISSUE_BA540_514A652BE1A)
- [AWS Outage Analysis: October 20, 2025](https://www.thousandeyes.com/blog/aws-outage-analysis-october-20-2025)
- [Amazon's massive AWS outage points to a key weakness in the modern internet](https://finance.yahoo.com/news/amazons-massive-aws-outage-points-to-a-key-weakness-in-the-modern-internet-145418180.html)
- [What caused Amazon's AWS outage, and why did so many major apps go offline?](https://www.aljazeera.com/news/2025/10/21/what-caused-amazons-aws-outage-and-why-did-so-many-major-apps-go-offline)
- [AWS Outage on October 20: How a DNS Glitch in DynamoDB Disrupted the Internet](https://medium.com/@ansababy/aws-outage-on-october-20-how-a-dns-glitch-in-dynamodb-disrupted-the-internet-40e1f0440a12)
- [Update - AWS services operating normally](https://www.aboutamazon.com/news/aws/aws-service-disruptions-outage-update)
- [AWS was down — live updates following massive outage](https://www.tomsguide.com/news/live/amazon-outage-october-2025)
