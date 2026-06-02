---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Alibaba Replaces IBM Oracle EMC
translated: false
type: note
---

### Alibaba's "Remove IOE" Initiative

Alibaba's "Remove IOE" (or "去IOE") campaign, launched around 2008-2009, was a strategic effort to eliminate dependency on proprietary vendor stacks from **IBM**, **Oracle**, and **EMC** (IOE acronym). The goal was to reduce costs, improve scalability, and foster innovation by shifting to open-source and in-house developed technologies. This was crucial for Alibaba's e-commerce growth, as IOE systems were expensive and less flexible for massive scale.

#### What Was Removed: The IOE Stack

The "IOE" referred to a tightly integrated, high-end enterprise stack dominated by these vendors. Here's a breakdown of the key components Alibaba phased out:

1. **IBM (Hardware and Middleware)**:
   - **Main Components Removed**:
     - IBM mainframes (e.g., zSeries or System z) and high-end servers like Power Systems.
     - IBM's AIX operating system (proprietary Unix variant).
     - IBM WebSphere (application server/middleware for Java apps).
     - IBM DB2 database in some cases (though Oracle was the primary target for databases).
   - **Why Removed?** IBM hardware was reliable but costly, lock-in heavy, and not optimized for cloud-scale horizontal scaling. Alibaba replaced it with cheaper, commodity x86 hardware (e.g., Intel/AMD servers running Linux).

2. **Oracle (Database)**:
   - **Main Components Removed**:
     - Oracle Database (enterprise relational database, e.g., Oracle 10g/11g RAC for high availability).
     - Oracle middleware like Oracle Fusion Middleware or WebLogic Server.
   - **Why Removed?** Licensing fees were exorbitant (scaling with CPU cores and users), and it wasn't ideal for Alibaba's massive read/write workloads (e.g., Taobao's transaction spikes). Oracle's proprietary nature limited customization.

3. **EMC (Storage)**:
   - **Main Components Removed**:
     - EMC Symmetrix or Clariion storage arrays (SAN/NAS enterprise storage systems).
   - **Why Removed?** Expensive proprietary storage with vendor lock-in; hard to scale linearly for petabyte-level data in e-commerce.

The overall IOE stack was a "closed" ecosystem: IBM servers running AIX, Oracle DB on top, stored on EMC arrays, with IBM middleware gluing it together. This was common in traditional enterprises but a bottleneck for Alibaba's needs.

#### What Replaced the IOE Stack

Alibaba rebuilt everything on open-source foundations, commodity hardware, and custom developments. Key replacements:

- **Hardware/OS Layer (Replacing IBM)**:
  - Commodity x86 servers (e.g., from Dell, HP, or custom-built).
  - Linux distributions (initially CentOS/RHEL; later Alibaba Cloud's own ALINUX).
  - In-house orchestration tools for cluster management.

- **Database Layer (Replacing Oracle)**:
  - **Open-Source Start**: MySQL (Alibaba contributed heavily; it's now a fork of MySQL 5.5/5.6 with AliSQL patches for high concurrency).
  - **Custom Developments**:
    - **OceanBase**: Alibaba's distributed relational database (NewSQL), designed for financial-grade reliability (supports ACID transactions at massive scale). It's now open-source and used in Ant Group's Alipay.
    - Tair/DRDS: In-memory caching (like Redis) and distributed SQL sharding for horizontal scaling.
  - This allowed handling billions of queries daily without Oracle's licensing costs.

- **Storage Layer (Replacing EMC)**:
  - Ceph or HDFS-based distributed storage.
  - Alibaba's PolarFS or custom block/object storage on commodity disks.
  - Later evolved into Alibaba Cloud OSS (Object Storage Service) and EBS (Elastic Block Store).

- **Middleware/Application Layer**:
  - HSF (High-Speed Service Framework) for microservices (replacing WebSphere).
  - Apache Dubbo for RPC/service discovery.
  - In-house tools like SOFA (Scalable Open Framework Architecture).

#### Impact and Legacy

- **Cost Savings**: Reduced hardware/database costs by 70-80% initially.
- **Scalability**: Enabled Alibaba to handle Double 11 (Singles' Day) peaks (e.g., 500,000+ orders/second).
- **Innovation**: Sparked Alibaba's cloud business (Alibaba Cloud, now the world's largest by some metrics) and open-source contributions (e.g., OceanBase is used by banks globally).
- **Timeline**: Fully transitioned by around 2012-2015; "Remove IOE" became a mantra for Chinese tech firms.

If you're asking about specifics (e.g., migration challenges or current Alibaba stack), let me know for more details! Sources: Alibaba's official blogs, Jack Ma's talks, and tech reports from that era.
