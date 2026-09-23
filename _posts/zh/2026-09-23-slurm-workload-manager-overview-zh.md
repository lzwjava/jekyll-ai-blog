---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Slurm工作负载管理器概述
translated: true
type: note
---

本项目是 **Slurm工作负载管理器** — 用于高性能计算（HPC）环境的开源集群资源管理与作业调度系统。

## 功能概述

作为集群资源管理器，Slurm提供三大核心功能：

1. **资源分配** — 在指定时间内为用户分配计算节点的独占/非独占访问权限。
2. **作业执行框架** — 在分配节点上启动、执行并监控工作（通常为并行作业）。
3. **作业调度/仲裁** — 管理待处理作业队列并解决资源冲突请求。

## 主要特性

- 开源，采用GPL许可证
- 设计简洁、可扩展、可移植、容错性强、与互连架构无关
- 运行于Linux系统

## 仓库结构

- `src/` — Slurm核心源代码（按子目录组织，如`src/api`、`src/slurmctld`）
- `doc/` — 文档、指南和手册页
- `etc/` — 示例配置文件和脚本
- `slurm/` — 已安装的公共头文件（`slurm.h`、`slurm_errno.h`、`slurmdb.h`、`pmi.h`、`spank.h`），用于编译基于Slurm API的程序
- `testsuite/` — 基于Check、Expect和Pytest框架编写的测试用例
- `auxdir/` — autotools构建脚本
- `contribs/` — Slurm核心之外的实用工具
- `CHANGELOG/` — 版本变更日志（此检出包含截至26.05版本的发布说明）

此为完整的Slurm源码发行版检出（包含autotools构建工具`configure`、`Makefile.in`等），而非部分镜像。
