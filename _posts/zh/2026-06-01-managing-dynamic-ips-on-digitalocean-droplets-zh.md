---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 管理DigitalOcean Droplet上的动态IP
translated: true
type: note
---

**问题：** 每次我在 AMD Developer Cloud（DigitalOcean）上创建 GPU Droplet 或从快照恢复时，公共 IPv4 地址都会发生变化——这是正常行为吗？

**回答：**

是的，这完全正常。原因如下：

## DigitalOcean Droplet 的临时 IP

DigitalOcean 在创建 Droplet 时**从 IP 池动态分配**公共 IPv4 地址。这意味着：

- **新 Droplet** → 从池中分配新 IP
- **Droplet 销毁后重建** → 不同 IP
- **从快照恢复** → 不同 IP（这是一个新的 Droplet 实例，只是带有你旧的磁盘状态）
- **关机后再开机** → IP **保持不变**（Droplet 仍然存在）

IP 与 Droplet 的*存在*绑定，而不是其*状态*。

## 快照恢复后保持不变的内容

当你恢复快照时，你会得到：
- ✅ 相同的文件系统、软件包、模型、配置
- ✅ 相同的 SSH 密钥（已嵌入镜像中）
- ❌ 不同的公共 IPv4
- ❌ 不同的 Droplet ID

## 实用解决方案：别再追逐 IP

既然你主要通过终端操作，最简洁的方案如下：

**方案 1：保留 IP（DigitalOcean 的静态 IP）**
```bash
# 通过 doctl 为你的 Droplet 分配一个保留 IP
doctl compute reserved-ip-action assign <reserved-ip> --droplet-id <id>
```
保留 IP 在 Droplet 重建后依然存在——你可以重新分配它。只要分配给运行中的 Droplet 就免费。

**方案 2：编写脚本更新 SSH 配置**
```bash
#!/bin/bash
# 创建 Droplet 后，获取新 IP 并更新 ~/.ssh/config
NEW_IP=$(doctl compute droplet get <droplet-name> --format PublicIPv4 --no-header)
sed -i '' "s/HostName .*/HostName $NEW_IP/" ~/.ssh/config
echo "已更新 SSH 配置：$NEW_IP"
```

**方案 3：使用 `doctl` 动态解析**
```bash
# 一行 SSH 命令，无需硬编码 IP
ssh $(doctl compute droplet get amd-gpu --format PublicIPv4 --no-header) -i ~/.ssh/your_key
```
添加到 `~/.zshrc` 或 `~/.bashrc`：
```bash
alias amd='ssh -i ~/.ssh/amd_key $(doctl compute droplet get amd-gpu --format PublicIPv4 --no-header)'
```

**方案 4：Tailscale（长期最佳）**

在你的快照镜像中安装 Tailscale——它会分配一个稳定的 `100.x.x.x` 地址，无论公共 IP 如何变化都不会改变：
```bash
# 在 Droplet 内部（嵌入快照）
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
```
之后始终通过 `ssh 100.x.x.x` 连接——即使 DigitalOcean 更改了你的公共 IP 也能正常工作。

## 给你的建议

既然你正在启动昂贵的 MI300X Droplet 并在使用后销毁以节省每小时约 2 美元的费用，**将 Tailscale 嵌入快照**是最简洁的方案。一次性设置，永远无需管理 IP。如果需要稳定的公共访问端点，可将 DigitalOcean 保留 IP 作为备用方案。