---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何创建AMD GPU Droplets
translated: true
type: note
---

**问题：** 我已经创建了一个 AMD 账户——具体要去哪里在 AMD Developer Cloud 上创建 GPU Droplet？

**回答：**

你所查看的 AMD 个人资料页面（`amd.com` 账户）**并非**创建 GPU Droplet 的地方。AMD Developer Cloud 是一个由 DigitalOcean 提供支持的**独立网站**。以下是详细步骤指南：

---

## 步骤 1：访问正确的网址

AMD Developer Cloud 可通过 **devcloud.amd.com** 访问——它最终会重定向到 DigitalOcean，因为 AMD Developer Cloud 依赖 DigitalOcean 提供云环境和 GPU Droplet。

👉 **访问：[https://devcloud.amd.com](https://devcloud.amd.com)**

---

## 步骤 2：登录 / 注册 AMD AI Developer Program

如果你已有 AMD 账户，直接登录并注册 AMD AI Developer Program 即可。新用户可在登录页面选择“创建账户”，同时设置 AMD 账户并完成注册。

注册 AMD AI Developer Program 后，你将获得 **100 美元免费 GPU 额度**（单台 MI300X 约可使用 50 小时）。

---

## 步骤 3：添加支付方式（必需）

在创建 GPU Droplet 之前，平台要求添加有效的支付方式，**即使你的额度足以支付全部费用**。不添加卡片，“创建 GPU Droplet”按钮将保持灰色。点击左侧边栏的 **Billing**，然后添加一张信用卡。你的额度会优先使用，信用卡仅作为超额的备用扣款方式。

---

## 步骤 第 4 步：申请免费额度（可选但推荐）

AMD 正在为符合条件的开发者提供 **25 小时免费云额度**，需申请并通过审核。要申请，请导航至 **“GPU Droplet Page”**，填写额度申请表。额度批准后，你将在 droplet 页面看到“credits applicable”提示。

---

## 步骤 5：创建 GPU Droplet

登录后，你将被引导至 **创建 GPU Droplet** 页面，你的额度应显示在页面顶部。然后：

- **选择硬件：** 选择单台 MI300X 实例
- **选择镜像：** 选择 ROCm Software 镜像（或 vLLM Quick Start，如果你想要一个开箱即用的 LLM 堆栈）
- **配置访问：** 添加你的 SSH 密钥

Droplet 大约需要 **2–4 分钟** 完成配置。你将在仪表盘中看到状态从“Creating”变为“Active”。建议选择 **ATL1（亚特兰大）** 区域，该区域 MI300X 可用性稳定。

---

## 步骤 6：连接到你的 Droplet

状态变为“Active”后，你可以通过以下方式连接：

- **SSH** 从终端：`ssh root@<your-droplet-ip>`
- 直接在仪表盘中点击仪表盘中的 **Web Console** 按钮直接访问
- **JupyterLab** 环境（若你选择了该镜像——可通过浏览器直接访问，无需额外设置）

---

## 重要计费提醒

当你 **关机** GPU 虚拟机时，**仍会被计费**，因为你的磁盘空间、CPU、内存和 IP 地址均被保留。只有在 **销毁** 实例后，计费才会停止。

完成使用后，请务必 **销毁**（而非仅关机）droplet 以避免继续计费。

---

## 价格参考

| 配置 | 价格 |
| --- | --- |
| 1x AMD Instinct MI300X（192 GB VRAM） | $1.99/小时 |
| 8x AMD Instinct MI300X（1536 GB VRAM） | $15.92/小时 |
| 免费额度（AMD AI Developer Program） | ~$100（约 50 小时） |

---

**参考链接：**

- [AMD Developer Cloud 官方页面](https://www.amd.com/en/developer/resources/cloud-access/amd-developer-cloud.html)
- [如何开始使用 AMD Developer Cloud（AMD 博客）](https://www.amd.com/en/developer/resources/technical-articles/2025/how-to-get-started-on-the-amd-developer-cloud-.html)
- [AMD Developer Cloud 教程 – Lablab.ai](https://lablab.ai/ai-tutorials/amd-developer-cloud-host-llm-vllm)
- [Phoronix 对 AMD Developer Cloud 的评测](https://www.phoronix.com/review/amd-developer-cloud)
