---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RHEL企业版Linux完全指南
translated: true
type: note
---

以下是 **Red Hat Enterprise Linux (RHEL) 的完整指南**。我将按步骤构建，方便您既可作为学习路径，也可作为参考手册。

---

## 1. Red Hat Linux 简介

Red Hat Enterprise Linux (RHEL) 是由 **Red Hat 公司** 开发的商业 Linux 发行版，专为 **稳定性、安全性和企业级技术支持** 而设计。凭借其长期支持生命周期和经过认证的软件生态，该系统被广泛应用于金融、医疗、政府及企业 IT 领域。

核心亮点：

* 企业级技术支持（每个主版本支持周期超过 10 年）
* 通过主流硬件平台认证（戴尔、惠普、IBM 等）
* 广泛应用于云平台（AWS、Azure、GCP）、容器（OpenShift、Kubernetes）及虚拟化环境

---

## 2. 系统安装与配置

* **获取安装介质**：通过 Red Hat 客户门户下载官方 ISO 镜像（需订阅账户）
* **安装程序**：使用支持图形化与文本模式的 **Anaconda 安装程序**
* **磁盘分区**：支持 LVM、XFS（默认文件系统）及磁盘加密
* **初始化工具**：使用 `subscription-manager` 完成系统注册

---

## 3. 软件包管理

* **RPM** - 底层软件包格式
* **DNF** - RHEL 8 及以上版本的默认包管理器

  * 安装软件包：

    ```bash
    sudo dnf install httpd
    ```

  * 系统更新：

    ```bash
    sudo dnf update
    ```

  * 软件包搜索：

    ```bash
    sudo dnf search nginx
    ```

RHEL 同时支持 **应用流** 功能，可并行管理多版本软件（如 Python 3.6 与 3.9）

---

## 4. 系统管理基础

* **用户管理**：
  `useradd`、`passwd`、`usermod`、`/etc/passwd`、`/etc/shadow`
* **进程管理**：
  `ps`、`top`、`htop`、`kill`、`systemctl`
* **磁盘管理**：
  `lsblk`、`df -h`、`mount`、`umount`、`fdisk`、`parted`
* **系统服务管理**：

  ```bash
  systemctl start nginx
  systemctl enable nginx
  systemctl status nginx
  ```

---

## 5. 网络配置

* 配置文件存储路径：`/etc/sysconfig/network-scripts/`
* 常用命令：

  * `nmcli`
  * `ip addr`、`ip route`、`ping`、`traceroute`
* 防火墙管理：

  * 使用 **firewalld** 服务（操作命令 `firewall-cmd`）
  * 配置示例：

    ```bash
    firewall-cmd --add-service=http --permanent
    firewall-cmd --reload
    ```

---

## 6. 安全防护

* **SELinux**：强制访问控制系统

  * 状态检查：`sestatus`
  * 运行模式：强制模式、宽容模式、禁用模式
* **FirewallD**：网络防火墙管理
* **系统更新**：通过 `dnf update` 获取安全补丁
* **Auditd**：系统审计与合规性记录

---

## 7. 日志与监控

* **系统日志**：
  存储目录 `/var/log/`
* **Journald**：
  `journalctl -xe`
* **性能监控工具**：

  * `sar`（需安装 sysstat 软件包）
  * `vmstat`、`iostat`、`dstat`
* **Red Hat Insights**：云端系统分析平台

---

## 8. 虚拟化与容器

* **KVM**：基于内核的虚拟化技术
* **Podman**：容器运行时工具

  ```bash
  podman run -it centos /bin/bash
  ```

* **OpenShift**：基于 Kubernetes 的容器编排平台

---

## 9. 存储管理

* **LVM**：逻辑卷管理器，实现灵活磁盘管理
* **XFS**：默认文件系统
* **Stratis**：支持精简配置与快照的存储管理方案

---

## 10. 自动化与配置管理

* **Ansible**：Red Hat 自动化运维平台
* **Kickstart**：操作系统无人值守安装
* **系统角色**：预定义的 Ansible 角色库

---

## 11. 订阅与技术支持

* Red Hat 采用 **订阅服务模式**
* 使用 `subscription-manager` 进行系统注册、订阅关联与软件源启用
* 开发者订阅计划 **向个人用户免费开放**

---

## 12. 最佳实践

* 持续安装安全更新补丁
* 非调试场景下保持 SELinux 强制模式
* 使用 `rsyslog` 或 ELK 栈实现日志集中管理
* 通过 Ansible 实现重复任务自动化
* 利用 Red Hat Insights 监控系统健康状态

---

## 13. 学习资源

* [Red Hat 官方文档](https://access.redhat.com/documentation)
* [Red Hat 学术计划](https://www.redhat.com/en/services/training-and-certification/red-hat-academy)
* 认证体系：

  * **RHCSA**（红帽认证系统管理员）
  * **RHCE**（红帽认证工程师）
  * **RHCA**（红帽认证架构师）

---

✅ 以上是知识体系基础。
是否需要我将本指南 **扩展为实战手册**（包含建站、数据库配置、防火墙设置等实操流程），或保持 **理论概念导向** 的现有风格？
