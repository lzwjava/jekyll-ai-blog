---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cheap Fleet Distributed Computing Experiments
translated: false
type: note
---

Question: What experiments or projects can we build with a fleet of cheap (~500-1000 CNY) machines using Docker, distributed computing, and Spark?

Answer:

Great setup! Here's a breakdown of interesting experiments organized by theme:

---

## 🖥️ Cluster & Distributed Computing

- **Hadoop/Spark Cluster** — Distribute datasets across nodes, run MapReduce jobs, benchmark throughput vs. single-node
- **Ray Cluster** — Distributed ML training, hyperparameter tuning with Ray Tune
- **Dask Distributed** — Parallel pandas-style data processing across all nodes
- **MPI experiments** — Classic HPC-style parallel programs (matrix multiply, N-body simulation)

---

## 🧠 ML / AI Experiments

- **Federated Learning** — Simulate FL with each machine holding a private data shard; use Flower (`flwr`) framework
- **Distributed model training** — PyTorch DDP or Horovod across nodes
- **Parameter server architecture** — Build one from scratch to understand gradient sync
- **Hyperparameter search farm** — Each node tries different configs, reports to a central Optuna/MLflow server

---

## 📦 Infrastructure / DevOps

- **Kubernetes (K3s) on bare metal** — Lightweight k8s cluster, deploy microservices, test autoscaling
- **Docker Swarm** — Simpler alternative; deploy multi-container apps with rolling updates
- **Private container registry** — Host your own Harbor or Gitea+Docker registry
- **CI/CD pipeline** — Self-hosted Gitea + Drone/Woodpecker CI, run builds across agents

---

## 🌐 Networking & Systems

- **WireGuard mesh VPN** — Connect all nodes into a secure overlay network
- **Distributed DNS / service discovery** — Consul or CoreDNS experiments
- **BGP lab** — Run FRRouting on each node to simulate real-world routing
- **CDN simulation** — Nginx on each node serving cached content, benchmark cache hit rates

---

## 📊 Data Engineering

- **Kafka + Flink pipeline** — Simulate real-time event streaming and processing
- **ELK / Loki stack** — Centralized logging from all nodes; visualize in Grafana
- **MinIO distributed object storage** — Build your own S3-compatible cluster
- **ClickHouse cluster** — Distributed OLAP queries on large datasets

---

## 🔬 Research-Level Experiments

- **Blockchain / consensus algorithms** — Run Raft, Paxos, or a toy blockchain across nodes
- **Chaos engineering** — Kill nodes randomly, measure system resilience (use Chaos Monkey / Pumba)
- **Benchmarking study** — Measure how Spark/Ray/Dask scale with N nodes (great for a paper or blog)
- **IPFS node cluster** — Experiment with content-addressed distributed storage

---

## 💡 Recommended Starter Stack

| Layer | Tool |
| --- | --- |
| OS | Ubuntu Server (minimal) |
| Orchestration | K3s or Docker Swarm |
| Compute | Apache Spark or Ray |
| Storage | MinIO |
| Monitoring | Prometheus + Grafana |
| Networking | WireGuard |

---

References:

- [Apache Spark Cluster Mode](https://spark.apache.org/docs/latest/cluster-overview.html)
- [K3s - Lightweight Kubernetes](https://k3s.io/)
- [Flower - Federated Learning Framework](https://flower.dev/)
- [Ray - Distributed Python](https://docs.ray.io/en/latest/)
- [MinIO Distributed Setup](https://min.io/docs/minio/linux/operations/install-deploy-manage/deploy-minio-multi-node-multi-drive.html)
- [Chaos Mesh / Pumba](https://github.com/alexei-led/pumba)
