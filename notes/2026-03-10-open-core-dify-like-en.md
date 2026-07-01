---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open Core Companies Like Dify
translated: false
type: note
---

**Question:** What other companies follow a similar arrangement as Dify (open-source project + cloud portal + enterprise deployment)? For example, Elasticsearch and GreptimeDB?

---

**Answer:**

This model is called the **"Open-Core"** business model, and it is one of the most dominant strategies in modern developer-tool companies. The pattern is:

> **Free open-source core → Managed cloud SaaS → Enterprise on-prem/private deployment**

The public OSS businesses we see today like MongoDB, Confluent, and HashiCorp all employ a hybrid open-core / cloud-hosted model with professional services as an add-on.

---

## 1. Elasticsearch (Elastic)

The core of Elasticsearch and Kibana are open source under an AGPL license, and the code is housed in public repositories — you can get started or even build an entire solution without running code you can't see.

The three tiers:

- **Open Source / Self-hosted:** Free to run yourself on your own servers.
- **Elastic Cloud (SaaS):** Elastic Cloud enables engineering teams to take advantage of the features and benefits of Elasticsearch without requiring the expertise and maintenance involved. It follows a subscription, pay-as-you-go model that enables teams to deploy and manage an Elasticsearch cluster on AWS, Azure, or Google Cloud.
- **Enterprise (on-prem):** Advanced features are locked behind enterprise subscriptions — Standard, Gold, Platinum, and Enterprise tiers — building on top of the open-source core with advanced security (SAML/OIDC, field-level security), machine learning, cross-cluster replication, and alerting.

Notable drama: AWS began offering a managed Elasticsearch service, which collided with Elastic's business model. Elastic changed its licensing to prevent cloud providers from packaging Elasticsearch as a service, and AWS responded by forking the project and creating OpenSearch.

---

## 2. GreptimeDB (Greptime)

GreptimeDB is an open-source observability database that handles metrics, logs, and traces in one engine. It can be used as a single OpenTelemetry backend replacing Prometheus, Loki, and Elasticsearch, built on object storage.

The three tiers follow exactly the same pattern as Dify:

- **GreptimeDB OSS** — The open-sourced database for small to medium-scale observability and IoT use cases, ideal for personal projects or dev/test environments.
- **GreptimeDB Enterprise** — A robust observability database with enhanced security, high availability, and enterprise-grade support.
- **GreptimeCloud** — A fully managed, serverless DBaaS with elastic scaling and zero operational overhead, built for teams that need speed, flexibility, and ease of use out of the box.

---

## 3. HashiCorp (Terraform, Vault, Consul)

HashiCorp's open-source model evolved over time to include free, enterprise, and managed service versions. Products like Terraform, Vault, Consul, and Nomad are accessible through a source-available license, and many also have enterprise offerings and managed service offerings, with both free and paid tiers.

- **Open Source:** Terraform (IaC), Vault (secrets), Consul (networking) — free to self-host.
- **Enterprise:** Adds RBAC, audit logging, centralized management, and governance features.
- **HCP (HashiCorp Cloud Platform):** Fully managed SaaS versions of all tools.

HashiCorp went public in 2021 and was later acquired by IBM in February 2025 for $6.4 billion — a powerful validation of the open-core business model.

---

## 4. GitLab

GitLab CE (Community Edition) is under an MIT-style open source license, while GitLab EE (Enterprise Edition) is under a proprietary license.

GitLab took the open-core model and used it to build a complete, single-application DevOps platform — covering the entire software development lifecycle from project planning and CI/CD to security scanning and monitoring.

- **GitLab CE:** Free, self-hosted, open source.
- **GitLab.com (SaaS):** Free and paid tiers on their cloud portal.
- **GitLab EE:** Enterprise self-hosted with advanced features (compliance, SAML, audit events).

---

## 5. MongoDB

- **MongoDB Community Server:** Open source, self-hosted.
- **MongoDB Atlas:** MongoDB introduced Atlas, its cloud-hosted version, which has since become a monster business — making up approximately 60% of total revenue.
- **MongoDB Enterprise Advanced:** For on-premises or private cloud enterprise deployments with security, management, and support.

---

## 6. Confluent (Apache Kafka)

Apache Kafka is the open-source core. Confluent, founded by the original Kafka creators, layered on top:

- **Confluent Platform:** Self-hosted enterprise edition.
- **Confluent Cloud:** Fully managed Kafka-as-a-Service.
- Confluent Cloud grew over 200% year-over-year, demonstrating the effectiveness of this expansion model for companies with complex technologies that benefit from operational simplification.

---

## 7. Neo4j

Neo4j CE (Community Edition) is licensed under GPL version 3, while Neo4j EE (Enterprise Edition) is under a proprietary license, providing additional features including clustering and hot backups.

Same pattern: open community edition → hosted AuraDB cloud → enterprise on-prem.

---

## 8. Other Notable Examples

| Company / Project | Open Source Core | Cloud SaaS | Enterprise |
| --- | --- | --- | --- |
| **Supabase** | GitHub (Apache 2.0) | supabase.com | Self-hosted Enterprise |
| **Minio** | GitHub (AGPL) | Hosted object storage | AGPL / Commercial enterprise |
| **Airbyte** | GitHub (MIT/ELv2) | Airbyte Cloud | Self-Managed Enterprise |
| **Metabase** | GitHub (AGPL) | Metabase Cloud | Enterprise (SAML, SSO) |
| **n8n** | GitHub (Source-available) | n8n Cloud | Enterprise self-hosted |
| **DataStax** (Cassandra) | Apache Cassandra (open) | Astra DB Cloud | DataStax Enterprise |

---

## The Common Pattern Summarized

The second generation of OSS companies, known as open-core, provided two versions of their software: a "core" version that remained open source, and an enterprise version that utilized the core code but offered premium features such as security and integrations for a subscription. Over the past few years, OSS businesses have also incorporated an additional revenue stream through cloud-hosted services, allowing users to access the open-source binary via a cloud-hosted model instead of requiring them to set up and manage the product themselves.

The key differentiators for the enterprise tier are almost always the same set of features: SSO/SAML, RBAC, audit logging, high availability, dedicated support SLAs, and compliance tooling.

---

**References:**

- [Open-core model - Wikipedia](https://en.m.wikipedia.org/wiki/Open-core_model)
- [Elastic Open Source Philosophy](https://www.elastic.co/about/open-source)
- [GreptimeDB GitHub](https://github.com/GreptimeTeam/greptimedb)
- [Greptime Products Overview](https://www.greptime.com/product/db)
- [HashiCorp Open Source](https://www.hashicorp.com/en/about/open-source)
- [How companies make millions on Open Source (Palark)](https://palark.com/blog/open-source-business-models/)
- [Redpoint Open-source Top 25 Analysis](https://www.redpoint.com/content-hub/written/introducing-the-redpoint-open-source-top-25/)
