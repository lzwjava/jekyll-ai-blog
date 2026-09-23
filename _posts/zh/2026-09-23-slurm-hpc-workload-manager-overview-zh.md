---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Slurm HPC工作负载管理器概述
translated: true
type: note
---

Slurm 是一个功能全面的 HPC 集群工作负载管理器。基于代码库，以下是其按能力领域组织的功能：

## 核心作业生命周期
- **提交作业**（`sbatch`）——批处理脚本、作业数组、依赖关系、异构作业
- **运行交互式作业**（`srun`、`salloc`）——包括 `scrun`（OCI 容器运行时）
- **附加/加入运行中的作业**（`sattach`）
- **取消/发送信号给作业**（`scancel`）以及**等待作业**（`swait`）
- **作业步骤**——分配内的并行任务

## 资源管理与调度
- **分区（Partitions）**——具有不同策略的逻辑节点组（通过 `scontrol`、`sinfo`）
- **通用资源（GRES）**——GPU 及其他可调度设备（`src/plugins/gres`）
- **QoS**——具有限制的服务质量级别（`qos_functions.c`）
- **预留（Reservations）**——为维护或特定用户预留节点（`reservation_info.c`）
- **许可证（Licenses）**——跟踪和调度浮动软件许可证（`license_info.c`）
- **抢占（Preemption）**（`src/plugins/preempt`）和**优先级（Priority）**（`src/plugins/priority`）——公平份额、FIFO、多因子优先级
- **拓扑感知调度**（`src/plugins/topology`）和**节点特性**

## 计费与报告
- **作业计费（Job accounting）**（`sacct`）——跟踪 CPU、内存、能耗、文件系统、互连使用情况
- **数据库后端**（`slurmdbd`）——通过 `src/database` 使用 MySQL/MariaDB
- **关联/用户/账户管理**（`sacctmgr`）
- **报告（Reports）**（`sreport`）、**公平份额统计（Fair-share stats）**（`sshare`）、**优先级信息（Priority info）**（`sprio`）
- **归档（Archive）**支持长期计费数据

## 监控与控制
- **`sinfo`**——节点/分区状态；**`squeue`**——作业队列；**`sstat`**——实时作业统计；**`sdiag`**——诊断信息
- **`scontrol`**——管理控制（重新配置守护进程、修改节点/作业/分区等）
- **`sview`**——集群状态的图形界面
- **`strigger`**——事件触发器

## 高级功能
- **能耗/GPU 计费**（`src/plugins/acct_gather_energy`）
- **cgroup 支持**（`src/plugins/cgroup`）——资源隔离与限制
- **突发缓冲区（Burst buffers）**（`src/plugins/burst_buffer`）——数据暂存
- **作业数组、异构作业、作业依赖**
- **`scrontab`**——类 cron 的周期性作业
- **联邦集群（Federated clusters）**（`federation_info.c`、`federation_functions.c`）
- **PMI/PMIx**——用于 MPI 作业的进程管理接口（`slurm/pmi.h`、`pmi_server.c`）
- **REST API**（`slurmrestd` 位于 `src/`）——编程式 HTTP 接口
- **Lua 脚本**（`src/lua`）和**作业提交插件**（`src/plugins/job_submit`）——站点策略定制
- **MPI 支持**（`src/plugins/mpi`）——与 MPICH、OpenMPI 等的紧密集成
- **MCS、认证插件**（MunGE/authentication）、**TLS**（`src/plugins/tls`）、**压缩（Compress）**——安全与传输效率

## 可扩展性
- **SPANK**——用于作业启动定制的插件 API（`slurm/spank.h`）
- **C API**——用于构建自定义工具的完整库（`src/api`）
- **40 多种插件接口**——认证、计费、调度、选择、MPI、拓扑等

简而言之：它是 Linux 计算集群的完整调度 + 资源管理 + 计费栈，具有广泛的插件和 API 表面用于定制。