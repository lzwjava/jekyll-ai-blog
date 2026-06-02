---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 冗余Docker文件空间回收
translated: true
type: note
---

以下是完整的故事：

**来源：** AMD 开发云环境在创建 GPU 实例时预加载（2026 年 5 月 20 日）。

**占用 59GB 的内容：**

| 项目 | 大小 | 说明 |
|------|------|------|
| `rocm:latest` 镜像 | 36 GB | 容器中的 ROCm 7.2.0 GPU 栈（与宿主机 `/opt/rocm-7.2.0/` 相同） |
| 构建缓存 | 36 GB | 14 个过时的构建层（均已超过 2 个月，100% 可回收） |
| `ubuntu:24.04` 镜像 | 119 MB | Ubuntu 基础镜像 |
| `rocm` 容器 | 115 KB | 11 天前已退出，运行过 Jupyter Lab |

**`rocm` 容器的操作：**

- 运行 `jupyter lab`，具有 ROCm GPU 访问权限，笔记本目录为 `/home/rocm-user/jupyter`
- 创建于 5 月 20 日，约 5 月 21 日退出
- 日志显示有机器人扫描 PHP 漏洞（常见的网络流量，进入了暴露的 Jupyter 端口）

**关键发现：** `rocm:latest` 容器镜像与宿主机上已安装在 `/opt/rocm-7.2.0/`（根磁盘占用 22GB）的内容**重复**。容器镜像 + 宿主机安装 = 约 58GB 的冗余 ROCm 文件。

**可以安全删除的内容：**

- `docker container prune` — 移除已退出的 `rocm` 容器（节省约 115KB）
- `docker builder prune --all` — 移除 36GB 的过时构建缓存（节省 **36 GB**）
- `docker rmi rocm:latest` — 移除容器镜像（节省 **36 GB**），因为 ROCm 已安装在宿主机上

总计可回收：**约 72 GB** 的根磁盘空间。要我执行吗？
