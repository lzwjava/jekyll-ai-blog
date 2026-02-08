---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 家庭实验室：混乱与学习
translated: true
type: note
---

**Question:** 假设我家里有一台 Mac 和 2 台 Ubuntu 笔记本电脑。除了为了学习目的运行 Kafka 和 ZooKeeper，我还可以做哪些程序或有趣的项目？还有其他酷炫的事情可以做吗？

**Answer:**

你拥有一个非常棒的异构环境（macOS + Linux），非常适合作为一个小型 Home Lab 或分布式 Playground。Kafka + ZooKeeper（或是不需要 ZooKeeper 的现代 KRaft 模式）是学习 Streaming / Event-driven systems 的一个扎实起点，但利用这三台机器，你还可以构建更多有趣、搞怪或实用的项目。

以下是一些想法，按从“快速幽默”到“严肃学习/实用”的顺序排列：

### 幽默 / 搞怪 / “为什么不呢？”项目

- **分布式无用计算集群**  
  将三台机器变成一个微型“超级计算机”，共同浪费电能：在三台机器上运行 BOINC (SETI@home 风格)、Folding@home，或者挖掘一些玩笑性质的 Cryptocurency（或者只是用搞怪脚本模拟 Mining）。加分项：编写一个 Python 脚本，在机器之间进行 Ping 测试，并在 Mac 屏幕上显示虚假的“算力”统计数据。

- **过度设计的家庭 Meme / 通知系统**  
  在一台 Ubuntu 上运行 ntfy.sh 或 Gotify 服务器。在所有机器（包括 Mac）上编写微型脚本发送荒唐的通知：“老爸的 Mac 又打开 Reddit 了”、“Ubuntu-2 CPU 占用 0.1% —— 它在午睡”，或者通过 Cron 每小时发送 Meme 语录。在 Mac 上使用 `say` 或 `afplay` 添加音效。

- **多房间混乱音乐 / 音频服务器**  
  在一台 Ubuntu（服务端）上运行 Mopidy 或 Jellyfin + Snapcast，通过 Mac/iPhone 进行控制，并在所有三台笔记本电脑（如果都有扬声器）之间同步音频播放。随处播放同一首歌 → 瞬间获得令人烦躁的家庭环绕声系统。或者让一台机器成为“DJ Troll”，随机更改音量或播放列表。

- **零 IoT 设备的虚假智能家居**  
  使用 Home Assistant（在一台 Ubuntu 上），但控制虚假的“设备”：编写伪装成灯光的脚本（更改 Terminal 颜色）、咖啡机（打印 ASCII 咖啡图）或扫地机器人（在 Mac 上随机移动鼠标光标）。

### 酷炫且真正有用的学习项目

- **微型 Kubernetes / 容器编排 Playground**  
  在所有三台机器上安装 k3s（轻量级 Kubernetes） → 一台作为 Master（可以是带有 Multipass VM 或 kind 的 Mac），两台 Ubuntu 作为 Worker。部署一些有趣的东西，比如 404-game、自动伸缩的 Minecraft server pods，或者分布式的“随机语录”服务。

- **自托管个人云技术栈**  
  - Ubuntu-1：Nextcloud 或 Immich (照片) + PostgreSQL/MariaDB  
  - Ubuntu-2：MinIO (S3-compatible 对象存储) 或虚拟机中的 TrueNAS SCALE  
  - Mac：作为客户端 + 通过 SMB/NFS 作为 Time Machine 备份目标到其中一台 Ubuntu  
  在所有设备间私密地同步文件和照片。

- **分布式任务队列实验**  
  超越 Kafka/ZooKeeper：  
  - 在机器间配置 Celery + Redis/RabbitMQ  
  - 或者使用 Dask.distributed：Mac 作为 Scheduler，两台 Ubuntu 作为 Worker → 运行高度并行的 Python 任务（图像处理、ML training 块、密码破解演示、在各节点间渲染 Mandelbrot 集）。

- **过度配置的监控与可观测性 (Observability)**  
  在一台 Ubuntu 上部署 Prometheus + Grafana，在三台机器上部署 node-exporter → 制作精美的 Dashboard 展示 CPU、有趣的指标（如“Mac 上打开的 Safari 标签页数量”）、如果传感器工作则展示温度，以及炫耀 Uptime。

- **GitLab / Gitea + CI/CD Playground**  
  在一台 Ubuntu 上自托管 Gitea 或完整的 GitLab。在所有三台机器（包括 Mac Runner）上设置 GitLab Runner。练习 Pipeline：构建 Docker images、部署玩笑网站或自动备份你的 dotfiles。

- **多媒体与备份堡垒**  
  在 Ubuntu-1 上部署 Jellyfin / Plex (Media Server)，通过 Syncthing 或 rsync 从 Mac 同步媒体文件夹。在所有机器上使用 restic/BorgBackup → 互相进行加密备份（预算有限的情况下的 3-2-1 原则）。

- **学习基础 Kafka 之外的现代数据/流处理**  
  - Redpanda（Kafka-compatible，且更易配置）  
  - Apache Flink 或 Spark 集群（微型规模），用于处理虚假的 Streaming Data（例如 Twitter 风格的 Feed 模拟器）  
  - 用于跨机器工作流编排的 Temporal.io 或 n8n

- **网络安全 Playground**  
  将一台 Ubuntu 作为 pfSense/OPNsense 路由器/防火墙（需要第二个网卡），Mac 和另一台 Ubuntu 放在它后面 → 实验 VLAN、机器间的 WireGuard VPN、入侵检测 (Suricata) 或用于广告拦截的 Pi-hole。

从小处着手：挑选一个项目，为了保持一致性在各处使用 Docker/Podman（Mac 对两者都支持），从 Mac 使用 Ansible 来管理两台 Ubuntu 盒子。最大的乐趣往往源于对一些愚蠢事物的过度工程化 —— 这正是 Home Lab 的精神所在！

**References:**

- [https://github.com/mikeroyal/Self-Hosting-Guide](https://github.com/mikeroyal/Self-Hosting-Guide)
- [https://awesome-selfhosted.net/](https://awesome-selfhosted.net/)
- [https://www.youtube.com/watch?v=prg6-sYlijM](https://www.youtube.com/watch?v=prg6-sYlijM)
- [https://b3n.org/homelab-ideas](https://b3n.org/homelab-ideas)
- [https://selfh.st/apps](https://selfh.st/apps)