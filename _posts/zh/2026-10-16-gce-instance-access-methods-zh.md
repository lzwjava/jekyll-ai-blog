---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GCE实例访问方法
translated: true
type: note
---

访问Google Cloud（GCE）实例有几种方式：

## 1. 通过gcloud CLI进行SSH（最常见）

```bash
# 按名称SSH登录Linux实例
gcloud compute ssh INSTANCE_NAME --zone ZONE

# 例如：
gcloud compute ssh my-web-server --zone us-central1-a
```

在Windows上，这使用你的SSH密钥；首次连接时，OS Login或元数据SSH密钥会自动处理身份验证。

## 2. 从Cloud Console（浏览器）进行SSH

1. 在[控制台](https://console.cloud.google.com/compute/instances)中转到 **Compute Engine → VM实例**
2. 点击实例旁边的 **SSH** — 会在浏览器中打开一个终端
3. 适用于本地未安装gcloud CLI的情况

## 3. 使用你自己的SSH客户端

```bash
# 首先获取外部IP
gcloud compute instances describe INSTANCE_NAME --zone ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)'

# 然后直接连接
ssh username@EXTERNAL_IP
```

用户名取决于操作系统镜像：
- Debian/Ubuntu → 你配置的 `username`（或你的OS Login邮箱）
- CentOS/RHEL → `your_username`
- Container-optimized OS → 实例元数据中的 `username`

## 4. RDP（Windows实例）

```bash
gcloud compute start-iap-tunnel INSTANCE_NAME 3389 --local-host-port=localhost:3389 --zone ZONE
```

然后使用RDP客户端连接到 `localhost:3389`。或者使用控制台的 **重置密码** 加浏览器RDP选项。

## 前置条件检查清单

- `gcloud auth login` — 已完成身份验证
- `gcloud config set project PROJECT_ID` — 正确的项目
- 防火墙允许SSH：规则允许TCP端口 **22**（默认的 `default-allow-ssh` 规则已涵盖）
- 对于基于IAP的访问（推荐，无需外部IP）：
  ```bash
  gcloud compute ssh INSTANCE_NAME --zone ZONE --tunnel-through-iap
  ```

如果你告诉我你的操作系统类型以及是否安装了 `gcloud`，我可以给你准确命令。