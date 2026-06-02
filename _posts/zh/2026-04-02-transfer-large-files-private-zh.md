---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过私有网络传输大文件
translated: true
type: note
---

使用内部 10.xx 网络在 DigitalOcean Droplets 之间传输 60GB 文件是一种快速且免费移动数据的好方法，因为私有网络流量不计入您的带宽配额。

这是一个逐步指南来完成此操作。

### ✅ 步骤 1：确保您的 Droplets 在同一区域
私有 10.xx 网络仅可在位于**同一数据中心区域**的 Droplets 之间访问。在继续之前，请在 DigitalOcean Control Panel 中验证您的 Droplets 的位置。

### ✅ 步骤 2：验证私有网络接口
- **Standard Droplets**：使用接口 **`eth1`** 进行私有网络连接。
- **Multi-Node GPU Droplets**：使用高速 fabric NIC **`eth2` 到 `eth9`** 以获得最佳性能。
- **For Kubernetes (DOKS)**：高速 fabric 暴露为 **`fabric0` 到 `fabric7`**。

在每个 Droplet 上运行以下命令以确认私有 IP 地址（查找 `10.xx.xx.xx` 范围）：
```bash
ip -br addr
```

### ✅ 步骤 3：传输文件
对于一次性传输，最快的方法是使用 `scp`（Secure Copy Protocol）通过私有接口。

1.  **查找目标 Droplet 的私有 IP**
    - 您可以在 DigitalOcean Control Panel 的 Droplet 的“Settings”下找到它，或者在 Droplet 上运行 `ip -br addr`。

2.  **运行 SCP 命令**
    在**源 Droplet** 上，使用以下命令传输您的文件。用您的实际详细信息替换占位符。
    ```bash
    scp -r /path/to/your/source/file root@<destination_private_ip>:/path/to/destination/
    ```
    **示例：**
    ```bash
    scp -r /root/my-large-file.img root@10.100.0.5:/root/
    ```

### 💡 针对 60GB 文件的重要注意事项

- **使用 `screen` 或 `tmux`**：60GB 传输可能需要时间。在终端多路复用器如 `screen` 或 `tmux` 中运行传输，以防止 SSH 会话断开时传输停止。
- **设置 SSH 密钥**：为避免传输过程中提示输入密码，请在 Droplets 之间设置 SSH 密钥认证。您可以使用 `ssh-copy-id` 轻松复制公钥。
    ```bash
    ssh-copy-id root@<destination_private_ip>
    ```
- **传输时压缩**：如果您的文件尚未压缩，可以在传输过程中压缩以节省时间。但是，这会在两台服务器上使用 CPU。
    ```bash
    tar czf - /path/to/source-directory | ssh user@<private-ip> "tar xzf - -C /path/to/destination"
    ```
- **替代工具**：对于更快传输，尤其是非常大的文件，请考虑使用私有 IP 上的 `rsync`。它支持恢复中断传输。
    ```bash
    rsync -avz --progress /path/to/large-file user@<private-ip>:/destination/
    ```

### 🖥️ Multi-Node GPU Droplet 特定说明
如果您正在向 multi-node GPU Droplets（例如 H100 或 MI300X）传输数据或在它们之间传输，请记住：
- 高速 fabric（接口 `eth2` 到 `eth9`）专为**GPU-to-GPU 通信**设计（例如，用于 NCCL/RCCL）。对于使用 `scp` 或 `rsync` 的标准文件复制，操作系统通常会使用主要私有接口（`eth1`）。
- 要将高速 fabric 用于数据传输，您需要能够绑定到特定网络接口的专用工具，对于简单文件复制这是不必要的。标准私有网络（`eth1`）提供高达**25 Gbps** 的带宽，这对于 60GB 文件来说绰绰有余。
