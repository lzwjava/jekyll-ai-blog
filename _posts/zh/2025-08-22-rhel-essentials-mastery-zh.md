---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 精通红帽企业版Linux基础
translated: true
type: note
---

## Red Hat Linux 简介

Red Hat Enterprise Linux (RHEL) 是由红帽公司开发的领先开源操作系统。它专为企业环境设计，为关键任务应用提供稳定性、安全性和强大支持。RHEL 广泛应用于服务器、云环境和企业 IT 基础设施。

### 发展历程

- **1994年**：红帽 Linux 作为商业 Linux 发行版首次发布
- **2002年**：红帽推出企业级可靠性的 Red Hat Enterprise Linux
- **2025年**：RHEL 9 是最新主要版本，RHEL 10 正在开发中，提供增强安全性和容器支持等先进功能

### 核心特性

- **稳定性**：每个主要版本提供10年生命周期的长期支持(LTS)
- **安全性**：具备 SELinux（安全增强型Linux）、firewalld 和定期安全补丁
- **性能**：针对高性能计算、虚拟化和云部署进行优化
- **订阅模式**：通过红帽订阅提供更新、支持和认证软件访问
- **生态系统**：与 Red Hat OpenShift、Ansible 等 DevOps 和自动化工具集成

## 安装指南

### 系统要求

- **最低配置**：
  - 1.5 GB 内存
  - 20 GB 磁盘空间
  - 1 GHz 处理器
- **推荐配置**：
  - 4 GB 或更高内存
  - 40 GB 以上磁盘空间
  - 多核处理器

### 安装步骤

1. **下载 RHEL**：
   - 从[红帽客户门户](https://access.redhat.com)获取 RHEL ISO（需要订阅或开发者账户）
   - 非生产环境可使用免费开发者订阅
2. **创建启动介质**：
   - 使用 `dd` 或 Rufus 等工具创建可启动 U 盘
   - 示例命令：`sudo dd if=rhel-9.3-x86_64.iso of=/dev/sdX bs=4M status=progress`
3. **启动安装**：
   - 从 U 盘或 DVD 启动
   - 按照 Anaconda 安装程序指引：
     - 选择语言和区域
     - 配置磁盘分区（手动或自动）
     - 设置网络配置
     - 创建 root 密码和用户账户
4. **系统注册**：
   - 安装后通过订阅管理器注册：`subscription-manager register --username <用户名> --password <密码>`
   - 附加订阅：`subscription-manager attach --auto`

## 系统管理

### 软件包管理

RHEL 使用 **DNF**（Dandified YUM）进行软件包管理

- 安装软件包：`sudo dnf install <软件包名>`
- 系统更新：`sudo dnf update`
- 搜索软件包：`sudo dnf search <关键词>`
- 启用仓库：`sudo subscription-manager repos --enable <仓库ID>`

### 用户管理

- 添加用户：`sudo useradd -m <用户名>`
- 设置密码：`sudo passwd <用户名>`
- 修改用户：`sudo usermod -aG <用户组> <用户名>`
- 删除用户：`sudo userdel -r <用户名>`

### 文件系统管理

- 检查磁盘使用：`df -h`
- 列出挂载文件系统：`lsblk`
- 磁盘分区管理：使用 `fdisk` 或 `parted`
- 配置 LVM（逻辑卷管理器）：
  - 创建物理卷：`pvcreate /dev/sdX`
  - 创建卷组：`vgcreate <卷组名> /dev/sdX`
  - 创建逻辑卷：`lvcreate -L <大小> -n <逻辑卷名> <卷组名>`

### 网络配置

- 使用 `nmcli` 配置网络：
  - 列出连接：`nmcli connection show`
  - 添加静态 IP：`nmcli con mod <连接名> ipv4.addresses 192.168.1.100/24 ipv4.gateway 192.168.1.1 ipv4.method manual`
  - 激活连接：`nmcli con up <连接名>`
- 使用 `firewalld` 管理防火墙：
  - 开放端口：`sudo firewall-cmd --add-port=80/tcp --permanent`
  - 重载防火墙：`sudo firewall-cmd --reload`

### 安全配置

- **SELinux**：
  - 检查状态：`sestatus`
  - 设置模式（强制/宽容）：`sudo setenforce 0`（宽容模式）或 `sudo setenforce 1`（强制模式）
  - 修改策略：使用 `semanage` 和 `audit2allow` 定制策略
- **系统更新**：
  - 应用安全补丁：`sudo dnf update --security`
- **SSH 安全**：
  - 编辑 `/etc/ssh/sshd_config` 禁用 root 登录（`PermitRootLogin no`）并修改默认端口
  - 重启 SSH：`sudo systemctl restart sshd`

## 高级功能

### 容器与虚拟化

- **Podman**：RHEL 的无根容器工具
  - 运行容器：`podman run -it docker.io/library/centos bash`
  - 构建镜像：`podman build -t <镜像名> .`
- **虚拟化**：使用 `libvirt` 和 `virt-manager` 管理虚拟机
  - 安装：`sudo dnf install libvirt virt-manager`
  - 启动 libvirt：`sudo systemctl start libvirtd`

### Ansible 自动化

- 安装 Ansible：`sudo dnf install ansible`
- 创建剧本：

  ```yaml
  - name: 安装 Apache
    hosts: all
    tasks:
      - name: 安装 httpd
        dnf:
          name: httpd
          state: present
  ```

- 运行剧本：`ansible-playbook playbook.yml`

### 云集成

- RHEL 与 AWS、Azure 和 Google Cloud 集成
- 使用 Red Hat OpenShift 进行容器编排
- 通过 Red Hat Cloud Access 在云环境中部署 RHEL 镜像

## 故障排除

- **日志检查**：查看 `/var/log` 系统日志（如 `/var/log/messages` 或 `/var/log/secure`）
- **Systemd 管理**：使用 `systemctl` 管理服务：
  - 检查服务状态：`systemctl status <服务名>`
  - 重启服务：`systemctl restart <服务名>`
- **性能监控**：使用 `top`、`htop` 或 `vmstat` 监控系统性能
- **网络诊断**：使用 `ping`、`traceroute` 或 `nslookup` 进行网络诊断

## 最佳实践

- 定期更新系统修补漏洞
- 使用强密码并强制执行 SELinux 策略
- 使用 `rsync` 或红帽 `rear` 等工具备份关键数据
- 使用 Cockpit（`sudo dnf install cockpit`）等工具监控系统健康状态

## 资源链接

- [红帽客户门户](https://access.redhat.com)
- [RHEL 文档中心](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux)
- [红帽开发者计划](https://developers.redhat.com)
- [Red Hat Discuss](https://discuss.redhat.com) 等社区论坛
