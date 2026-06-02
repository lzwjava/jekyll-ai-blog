---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Introduction to GCP Cloud Load Balancing
translated: false
type: note
---

Question: What is an introduction to Cloud Load Balancing in Google Cloud Platform (GCP)?

Answer:

Cloud Load Balancing in **Google Cloud Platform (GCP)** is a fully managed, distributed, software-defined load balancing service. It distributes incoming traffic across multiple backend instances (such as Compute Engine VMs, Google Kubernetes Engine clusters, Cloud Run services, or VM instance groups) to ensure high availability, scalability, and performance.

### Key Characteristics

- **Fully distributed**: Uses Google's global **Anycast IP** infrastructure — the same frontend IP can be announced from many points of presence worldwide.
- **No pre-warming** required — it scales automatically with traffic.
- **Integrated health checking** — automatically removes unhealthy backends.
- **Zero-downtime configuration changes** in most cases.
- **Premium Tier** (global, uses Google's backbone) vs **Standard Tier** (regional, lower cost but uses public internet for some paths).

### Main Types of Load Balancers

Google Cloud offers several load balancer types. The two main categories are:

1. **Application Load Balancers** (Layer 7 – content-aware)
   - Understand HTTP/HTTPS/gRPC/HTTP/2/QUIC protocols
   - Support URL maps, host/path-based routing, traffic splitting, header-based routing, etc.
   - Sub-types:
     - **External Application Load Balancer** (global) → Classic choice for internet-facing web/apps
     - **Internal Application Load Balancer** (regional) → For private traffic inside VPC
     - **Cross-region Internal Application Load Balancer** (newer, multi-region internal HTTP(S))

2. **Network Load Balancers** (Layer 4 – protocol/port-based)
   - Pass traffic through with minimal inspection
   - Sub-types:
     - **External passthrough Network Load Balancer** (regional) → TCP/UDP/SSL proxy
     - **Internal passthrough Network Load Balancer** (regional) → TCP/UDP inside VPC
     - **TCP/SSL Proxy Load Balancer** (global) → Terminates SSL, preserves client IP

### Quick Comparison Table

| Load Balancer Type              | Scope     | Layer | Protocols                  | Typical Use Case                          | Preserves Client IP |
|---------------------------------|-----------|-------|----------------------------|-------------------------------------------|---------------------|
| External Application            | Global    | L7    | HTTP(S), HTTP/2, gRPC, QUIC| Public websites, APIs                     | Yes (with XFF)      |
| Internal Application            | Regional  | L7    | HTTP(S)                    | Internal microservices                    | Yes                 |
| TCP/SSL Proxy                   | Global    | L4    | TCP, SSL                   | Non-HTTP global TCP/SSL services          | Yes                 |
| External Passthrough Network    | Regional  | L4    | TCP, UDP                   | Gaming, VoIP, legacy protocols            | Yes (direct)        |
| Internal Passthrough Network    | Regional  | L4    | TCP, UDP                   | Internal TCP/UDP traffic                  | Yes (direct)        |

### Core Components

- **Frontend** — IP address + port + protocol (the entry point)
- **Backend service** — Defines how traffic is routed to backends + health checks + session affinity
- **Backend** — Instance groups, NEGs (Network Endpoint Groups), Cloud Run, etc.
- **URL map** (L7 only) — Host/path routing rules
- **Health checks** — Determine if backends are healthy
- **Autoscaling** — Works seamlessly with MIGs (Managed Instance Groups)

### Common Use Cases

- Distributing global user traffic to the nearest healthy instance (low latency)
- Blue/green deployments and canary releases via traffic splitting
- Exposing internal services securely within VPC
- Handling sudden traffic spikes (Black Friday, product launches)
- Supporting hybrid/multi-cloud setups via global external load balancing

Cloud Load Balancing is one of the most powerful and developer-friendly load balancing offerings among major cloud providers, especially for global applications.

References:

- [Cloud Load Balancing overview](https://docs.cloud.google.com/load-balancing/docs/load-balancing-overview)
- [Choose a load balancer](https://docs.cloud.google.com/load-balancing/docs/choosing-load-balancer)
- [Load balancer feature comparison](https://docs.cloud.google.com/load-balancing/docs/features)
- [Cloud Load Balancing product page](https://cloud.google.com/load-balancing)
