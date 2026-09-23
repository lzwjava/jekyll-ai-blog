---
audio: false
generated: true
image: false
lang: en
layout: post
title: Slurm HPC Workload Manager Overview
translated: false
type: note
---

Slurm is a full-featured HPC cluster workload manager. Based on the codebase, here's what it can do, organized by capability area:

## Core job lifecycle

- **Submit jobs** (`sbatch`) — batch scripts, arrays, dependencies, heterogeneous jobs
- **Run interactive jobs** (`srun`, `salloc`) — including `scrun` (OCI container runtime)
- **Attach/join running jobs** (`sattach`)
- **Cancel/signal jobs** (`scancel`) and **wait for jobs** (`swait`)
- **Job steps** — parallel tasks within an allocation

## Resource management & scheduling

- **Partitions** — logical groups of nodes with different policies (via `scontrol`, `sinfo`)
- **Generic resources (GRES)** — GPUs, and other schedulable devices (`src/plugins/gres`)
- **QoS** — quality-of-service levels with limits (`qos_functions.c`)
- **Reservations** — reserve nodes for maintenance or specific users (`reservation_info.c`)
- **Licenses** — track and schedule floating software licenses (`license_info.c`)
- **Preemption** (`src/plugins/preempt`) and **priority** (`src/plugins/priority`) — fair-share, FIFO, multifactor priority
- **Topology-aware scheduling** (`src/plugins/topology`) and **node features**

## Accounting & reporting

- **Job accounting** (`sacct`) — track CPU, memory, energy, filesystem, interconnect usage
- **Database backend** (`slurmdbd`) — MySQL/MariaDB via `src/database`
- **Association/user/account management** (`sacctmgr`)
- **Reports** (`sreport`), **fair-share stats** (`sshare`), **priority info** (`sprio`)
- **Archive** support for long-term accounting data

## Monitoring & control

- **`sinfo`** — node/partition state; **`squeue`** — job queue; **`sstat`** — live job stats; **`sdiag`** — diagnostics
- **`scontrol`** — administrative control (reconfigure daemons, modify nodes/jobs/partitions, etc.)
- **`sview`** — GUI view of cluster state
- **`strigger`** — event triggers

## Advanced features

- **Energy/GPU accounting** (`src/plugins/acct_gather_energy`)
- **cgroup support** (`src/plugins/cgroup`) — resource isolation and limits
- **Burst buffers** (`src/plugins/burst_buffer`) — data staging
- **Job arrays, heterogeneous jobs, job dependencies**
- **`scrontab`** — cron-like periodic jobs
- **Federated clusters** (`federation_info.c`, `federation_functions.c`)
- **PMI/PMIx** — process management interface for MPI jobs (`slurm/pmi.h`, `pmi_server.c`)
- **REST API** (`slurmrestd` in `src/`) — programmatic HTTP interface
- **Lua scripting** (`src/lua`) and **job submit plugins** (`src/plugins/job_submit`) — site policy customization
- **MPI support** (`src/plugins/mpi`) — tight integration with MPICH, OpenMPI, etc.
- **MCS, auth plugins** (MunGE/authentication), **TLS** (`src/plugins/tls`), **compress** — security & transfer efficiency

## Extensibility

- **SPANK** — plugin API for job launch customization (`slurm/spank.h`)
- **C API** — full library for building custom tools (`src/api`)
- **40+ plugin interfaces** — auth, accounting, scheduling, select, MPI, topology, etc.

In short: it's the complete scheduling + resource management + accounting stack for a Linux compute cluster, with extensive plugin and API surfaces for customization.
