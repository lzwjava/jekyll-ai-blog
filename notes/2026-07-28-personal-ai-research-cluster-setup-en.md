---
audio: false
generated: true
image: false
lang: en
layout: post
title: Personal AI Research Cluster Setup
translated: false
type: note
---

Question: **Is there software that lets me use 3–5 computers (some with GPUs) as a shared environment to run AI agent sessions, experiments, and research?**

Answer:

Yes. What you want is basically a **personal AI research cluster / agent workstation orchestration layer**. There are several approaches depending on whether you want:

1. **Run agents/jobs across machines**
2. **Share GPU compute**
3. **Manage experiments**
4. **Have one "brain" controlling multiple workers**

For your setup (RTX 4070 + other PCs + AI agents), I would look at these:

---

## 1. Ray — probably the closest match

Ray

Ray was built for exactly this:

* multiple machines
* CPU/GPU scheduling
* distributed Python workloads
* RL/LLM experiments
* agents

Architecture:

```
                 Ray Head Node
              (your main machine)
                      |
        +-------------+-------------+
        |             |             |
     Worker 1      Worker 2      Worker 3
     RTX 4070      RTX GPU       CPU only

        |             |             |
     LLM agent     training     evaluation
```

Example:

Machine A:

```bash
ray start --head --port=6379
```

Machine B/C/D:

```bash
ray start \
  --address='192.168.1.10:6379'
```

Then Python:

```python
import ray

ray.init()

@ray.remote(num_gpus=1)
class GPUWorker:
    def run(self):
        return "training on GPU"

worker = GPUWorker.remote()

print(ray.get(worker.run.remote()))
```

You can run:

* multiple Claude/OpenAI/local agents
* model evaluation
* fine-tuning jobs
* data processing

This is what many AI labs use internally.

---

## 2. Kubernetes + GPU scheduling

If you want a mini AI cloud:

```
                 Kubernetes
                     |
       +-------------+-------------+
       |             |             |
     PC1           PC2           PC3
   RTX4070       RTX GPU        CPU

       |
  vLLM / Ollama / Training / Agents
```

Stack:

* Kubernetes
* NVIDIA GPU Operator
* KServe
* vLLM
* Argo Workflows

More production-like.

For 3–5 home machines, however, Kubernetes is often overkill.

---

## 3. Slurm — HPC style

Slurm Workload Manager

Classic research cluster scheduler.

Used by:

* universities
* supercomputing centers
* AI labs

Example:

```
submit job

sbatch train.sh


Scheduler decides:

node1 GPU
node2 GPU
node3 CPU
```

Great for:

* GPT training
* distributed experiments
* sweeps

Less good for interactive agents.

---

## 4. Docker Swarm — simple home cluster

If you want something lightweight:

```
docker swarm init

docker swarm join
```

Then:

```
docker service create \
 --replicas 5 \
 my-agent
```

Good for:

* agent servers
* API workers
* databases

Not as good for GPU ML.

---

## 5. AI agent specific: OpenHands / SWE-agent style workers

For coding agents:

OpenHands

You can have:

```
Controller

 |
 +-- Agent worker 1
 |       coding task
 |
 +-- Agent worker 2
 |       test task
 |
 +-- Agent worker 3
        research task
```

Combine with Ray:

```
Ray
 |
 +-- Claude API agent
 +-- Qwen local agent
 +-- coding sandbox
 +-- evaluation worker
```

---

## 6. My recommended architecture for you

Given your history:

* RTX 4070
* trained GPT-2 locally
* building CLI agents
* running experiments
* multiple computers

I would build:

```
                 Mac / Laptop
              Agent Controller
                    |
                  Ray
                    |
       +------------+------------+
       |            |            |
    Ubuntu GPU   Windows GPU   CPU box

       |            |            |
    vLLM        Ollama        data jobs

       |
   Experiment DB
       |
   MLflow/W&B
```

Software:

| Purpose             | Tool                     |
| ------------------- | ------------------------ |
| cluster control     | Ray                      |
| containers          | Docker                   |
| local LLM serving   | vLLM / Ollama            |
| experiments         | MLflow                   |
| dataset processing  | Ray Data                 |
| agent orchestration | LangGraph / your own CLI |
| monitoring          | Prometheus + Grafana     |

---

## Minimal home version

Install Ray:

```bash
pip install ray
```

Head:

```bash
ray start --head
```

Workers:

```bash
ray start --address=<HEAD_IP>:6379
```

Now your 5 computers become one logical machine.

---

For an AI engineer building agents, I would choose:

**Ray first → add MLflow → add Docker → only later Kubernetes.**

It gives you 80% of an AI lab cluster with 20% of the complexity.

References:

* Ray documentation: [https://docs.ray.io/](https://docs.ray.io/)
* Slurm Workload Manager: [https://slurm.schedmd.com/](https://slurm.schedmd.com/)
* MLflow: [https://mlflow.org/](https://mlflow.org/)
* Kubernetes: [https://kubernetes.io/](https://kubernetes.io/)
