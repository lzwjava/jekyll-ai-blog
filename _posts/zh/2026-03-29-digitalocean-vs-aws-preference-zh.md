---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么开发者更倾向于选择 DigitalOcean 而非 AWS
translated: true
type: note
---

Question: 是否有些用户更倾向于选择 DigitalOcean 而非 GCP 和 AWS，是因为它更简单，能以良好的 bare metal 和 open source 自建选项满足需求，而 GCP 和 AWS 则增加了太多的 abstraction 和中间层？尽管 DigitalOcean 规模较小且功能较少，但考虑到 open source 的可用性，它是否足以应对大多数情况？

Answer:

是的，正如你所描述的，许多用户和开发者确实更倾向于选择 DigitalOcean (DO) 而非 Google Cloud Platform (GCP) 和 Amazon Web Services (AWS)。以下是具体的分析：

### 为什么用户喜欢 DigitalOcean 的简洁性
- **直观的基础设施**：DigitalOcean 专注于核心的 compute (Droplets)、storage (Volumes, Spaces) 和 networking，没有沉重的 managed services 层。你获得的是一种接近 bare metal 的纯净 VPS 或 VM 体验。许多用户表示它“好用且直观”，无需在复杂的控制面板或意外的 abstraction 中挣扎。
- **开发者友好的定价和体验**：Instance 非常易于理解（CPU、RAM、storage 都是透明的）。计费可预测，UI/CLI 非常简单。这对 startups、indie hackers、小团队以及想要避开“企业级臃肿”的开发者非常有吸引力。
- **Bare metal 和贴近硬件的感受**：虽然 DigitalOcean 主要以虚拟化的 Droplets 闻名，但它们提供良好的 performance，你可以轻松运行自己的 open source stack（如 Docker、通过 DOKS 运行 Kubernetes，但许多人更喜欢 self-managed）。该平台鼓励使用 Docker、Compose、Ansible、Terraform 等工具进行自建（self-setup）。

### 与 GCP 和 AWS 的对比
- **Abstraction 层**：AWS 和 GCP 提供数以百计（甚至数千计）的服务并进行深度集成。这对于大规模、复杂的 workload 非常强大，但往往会带来：
  - 更高的学习曲线（IAM roles、VPCs、像 EKS/GKE、Lambda、Cloud Run 这样的 managed services 等）
  - 通过专有服务引入的潜在 vendor lock-in
  - 额外的“中间层”（orchestration、auto-scaling groups、带有自身特性的 managed databases）
  - 即便是简单的 app，其 operational complexity 也会更高

  许多开发者抱怨，对于标准的 web apps、ML 实验或中小型的 production workloads，AWS/GCP 显得过度工程化（over-engineered）。

- **何时 DigitalOcean “足够用”**：
  是的，对于大部分使用场景——个人项目、SaaS startups、web apps、APIs、databases、CI/CD、小型 ML workloads——DigitalOcean 完全胜任。open source 生态系统（PostgreSQL、Redis、Nginx、Traefik、Prometheus、Grafana 等）填补了大部分空白。你可以在 DO Droplets 上可靠地 self-host 几乎所有内容。

  DigitalOcean 上流行的配置包括：
  - LAMP/LEMP stacks
  - Docker + Docker Compose
  - Self-managed Kubernetes（或像 k3s 这样的轻量级替代品）
  - Self-hosted GitLab
  - Nextcloud、ownCloud 等

  由于底层 OS 是标准的 Linux，你拥有完全的控制权，并且可以轻松地在不同 provider 之间复制配置。

### DigitalOcean 的局限性（为什么它规模较小）
- 较少的先进 managed services（例如，在相同规模下没有直接等同于 AWS Lambda、SageMaker 或 GCP 进阶 AI/ML 工具的服务）。
- 与 AWS/GCP 庞大的 data center 足迹相比，在某些地区的 global reach 较小。
- 扩展到极大型 Enterprise 级别（每秒数百万次请求、复杂的 multi-region 架构）可能需要更多手动工作。
- 进阶的 compliance、dedicated hardware 选项或 ultra-low latency networking 等企业级特性在 AWS/GCP 上更具优势。

然而，对于大多数**并非**处于 hyperscale 级别的用户和公司来说，这些局限性很少产生影响。许多成功的业务在 DigitalOcean 上稳定运行了多年。

### 谁通常更青睐 DigitalOcean？
- Indie 开发者和独立创始人
- 中小型 startups（尤其是 bootstrapped 自筹资金型）
- 重视简洁性和低认知负荷（cognitive load）的团队
- 相比 managed vendor services，更喜欢 open source self-hosting 的用户
- 来自传统 VPS providers（Linode、Vultr、Hetzner）并寻求现代但依然简单的 cloud 的用户

简而言之：你是对的。DigitalOcean 较少的功能集往往是一种优势而非劣势，因为它不会干扰你的操作，并允许 open source 工具处理其余工作。GCP 和 AWS 在极大型、复杂或高度受监管的环境中表现卓越，但对于大多数日常 workload，DO（或类似的简单 provider）已经“足够好”——而且通常使用体验更佳。

在开发者社区中，许多人会公开表示：“对于非企业级项目，我从 AWS 转向了 DigitalOcean，并且从未后悔。”

References:
- https://www.digitalocean.com/
- https://www.digitalocean.com/pricing
- https://www.reddit.com/r/webdev/comments/ (various threads comparing DO vs AWS)
- https://news.ycombinator.com/ (frequent discussions on DO simplicity)
