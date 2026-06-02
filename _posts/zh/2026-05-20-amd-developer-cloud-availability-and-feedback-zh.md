---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD开发者云可用性与反馈
translated: true
type: note
---

**问题：** AMD Developer Cloud MI300X Droplet（通过 DigitalOcean）的当前状态及近期可用性预测如何？Twitter/论坛上的社区反馈如何？

---

**回答：**

## AMD Developer Cloud — 当前状态与可用性预测（2026年5月）

### 底层架构

位于 `devcloud.amd.com` 的 AMD Developer Cloud 最终会重定向到 DigitalOcean。AMD 依靠 DigitalOcean 的基础设施提供 GPU Droplet。你所看到的 MI300X GPU Droplet 方案（$1.99/GPU/小时）实际上就是 DigitalOcean 的 GPU 产品，通过 AMD 的开发门户进行了白标（white-label）。

一个值得注意的怪异之处：尽管名为“AMD Developer Cloud”，其底层 CPU 主机却是 Intel Xeon Platinum 8568Y+（Emerald Rapids），而非 AMD EPYC。这一点被社区诟病，颇显讽刺。

---

### 当前硬件可用性（2026年5月）

**目前已可用的配置：**

- 1× MI300X — 192 GB VRAM，20 vCPU，240 GB RAM，5 TB NVMe — $1.99/小时
- 8× MI300X — 1.5 TB VRAM，160 vCPU，1920 GB RAM，40 TB NVMe — $15.92/小时（$1.99/GPU/小时）

**尚不可用的配置：**
截至平台于 2025 年 6 月推出时，尚无法访问 MI350 或 MI325X。Phoronix 的评测者指出，考虑到 MI350X/MI355X 同时发布，这一点令人惊讶。AMD 工程师也警告不要使用该云进行基准测试，因为可能存在噪声邻居（noisy neighbor）效应。

开箱即用的唯一 ROCm 版本是 ROCm 6.4.0，这已经落后于发布时的最新稳定版 6.4.1。

---

### 未来几个月的可用性预测

基于三个信号进行三角交叉验证：

**1. MI350 将登陆 ADC，但时间线不确定**
AMD 已承诺为 MI350 进行“Day-0”生态系统播种，合作方包括 vLLM、SGLang、HAO AI Lab 和 Stanford AI Lab。但这针对的是更广泛的云合作伙伴，不一定包含 ADC。Cirrascale 宣布其 AI Innovation Cloud 即将提供 MI350 系列，并开放了预览注册——这表明截至 2026 年 5 月，该服务尚未上线。

**2. MI300X 至少在 2026 年下半年仍将是主力**
目前有 9 家云提供商在 20 个列表中提供 MI300X。自 2025 年 5 月以来，按需定价上涨约 29%（整个市场每 GPU 从 $2.35 升至 $3.02/小时），但 AMD 自己的开发者云仍维持在 $1.99/小时。这一补贴很可能是为了推动 ROCm 的采用。

**3. AMD 正在积极扩大访问权限**
就在 2026 年 2 月，AMD 宣布未来一年为印度研究人员和初创公司提供 10 万小时的免费 ADC 使用时间。这表明 AMD 正在大力补贴 MI300X 使用时间以壮大 ROCm 生态系统——供应正在分配，而非缩减。

**预测：** ADC 上的 MI300X 将保持可用，并可能在 2026 年下半年变得*更容易*访问，因为 AMD 正在激励采用。基于当前信号，ADC 上的 MI350/MI355X 最早可能要到 2026 年下半年才会出现——AMD 仍在优先向主要合作伙伴进行生态播种。

---

### 社区反馈（论坛 / Twitter）

**优点：**
Phoronix 的 Michael Larabel 指出，启动非常快速简便——“进入 AMD Developer Cloud 几分钟内，我就成功启动了一个 Ubuntu 24.04 实例，运行着 ROCm 6.4.0 和八块 AMD Instinct MI300X 加速器。”

Docker 容器预装了流行的 AI 软件，并且 VM 启动后即可使用 Jupyter Notebook 环境，无需本地配置。

**缺点：**
一位 Phoronix 论坛用户记录了痛苦的入门摩擦：DigitalOcean 的反欺诈系统要求先有 3–4 笔已付费的账单记录，然后才能启用 GPU 访问。该用户总结道：“我需要先租用看起来是 Intel CPU 的实例 4 个月，然后这些守门神才认为我值得花钱租用 AMD GPU”——结论是 MI300X 的配额可能已经过度饱和。

**ROCm 软件差距：**
开箱即用的唯一选项是 ROCm 6.4.0（落后于最新稳定版）被视为一个问题。Phoronix 指出，希望 AMD 能够“及时更新操作系统映像，加入最新的 ROCm 预览版。”

**但生态系统势头确实存在：**
AMD 2026 年 5 月在旧金山举办的开发者黑客马拉松上出现了严肃的项目——定制 MI300X GPU 内核（在 CDNA3 上实现 2.4 倍加速的 MFMA GEMM 重写）、多代理 LLM 系统、vLLM-on-ROCm 推理栈。ROCm 社区正在基于它构建真正的东西。

---

### 给你的结论（智维）

如果你想**今天**就获得 MI300X 访问权限：

- **按需付费 $1.99/GPU/小时** 是最无摩擦的方式——但如果你的 DigitalOcean 账号是新的，其账单历史要求可能会先阻止你。
- 通过 AMD AI 开发者计划申请 **$100 免费额度**（强有力的用例（如使用 ROCm 进行训练/微调）会获得批准）。
- **其他零门槛提供商**：RunPod（$1.99/小时）、HotAisle（$1.99/小时）、TensorWave——同样的 MI300X，无需账单记录的把戏。

如果你计划进行 ROCm 内核开发或微调实验以对比 CUDA/H200 的经验，ADC + DigitalOcean 非常适合快速启动。只是不要将其用于性能基准测试（噪声邻居），并准备好自己在基础镜像上安装 ROCm 7.x。

---

**参考文献：**

- [试用 AMD Developer Cloud — Phoronix](https://www.phoronix.com/review/amd-developer-cloud)
- [Phoronix 论坛线程（账单摩擦）](https://www.phoronix.com/forums/forum/hardware/graphics-cards/1553509-trying-out-the-amd-developer-cloud-for-evaluating-instinct-rocm)
- [2026 年租用 AMD 云 GPU](https://cloud-gpus.com/amd-gpus/)
- [MI300X 云定价追踪器](https://getdeploying.com/gpus/amd-mi300x)
- [AMD Developer Cloud — 官方页面](https://www.amd.com/en/developer/resources/cloud-access/amd-developer-cloud.html)
- [AMD ROCm 7 + Developer Cloud 发布博客](https://www.amd.com/en/blogs/2025/enabling-the-future-of-ai-introducing-amd-rocm-7-and-the-amd-developer-cloud.html)
- [AMD 10 万小时印度计划](https://www.amd.com/en/blogs/2025/100k-hours-free-developer-cloud-access.html)
- [AMD 开发者黑客马拉松 SF 2026 年 5 月](https://lablab.ai/ai-hackathons/amd-developer)
