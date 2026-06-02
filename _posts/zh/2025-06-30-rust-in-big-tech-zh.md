---
audio: false
generated: true
lang: zh
layout: post
title: Rust在大科技公司的崛起
translated: true
type: note
---

Rust凭借其对内存安全、性能和并发性的高度关注，正在科技巨头领域获得显著发展。许多大型科技公司正在将Rust应用于各种关键项目。以下是部分知名案例的详细分析：

**1. 亚马逊（AWS）**

* **Firecracker**：专为安全运行大规模容器工作负载设计的微虚拟机，支撑着AWS Lambda和Fargate服务
* **AWS Nitro系统**：用于开发新组件，包括安全隔离的EC2环境
* **其他服务**：Rust被应用于Amazon S3、Amazon EC2、Amazon CloudFront和Amazon Route 53的组件开发
* **Bottlerocket**：基于Linux的容器操作系统，采用Rust编写

**2. 微软**

* **Windows组件**：正在积极使用Rust重写包括内核组件在内的Windows系统部件，以提升安全性与可维护性
* **Azure服务**：Rust已被集成到Azure IoT Edge和Kusto（Azure数据资源管理器的核心查询存储引擎）
* **`windows-rs`**：支持通过Rust调用Windows API的开源项目

**3. Meta（Facebook）**

* **内部源码管理工具**：使用Rust重构了内部源码控制系统Mononoke的组件，以更优的并发性能处理大型单体代码库
* **Diem区块链**：该加密货币项目的区块链主体采用Rust开发

**4. 谷歌**

* **Android开源项目**：越来越多地使用Rust编写安全系统组件，有效减少了媒体处理和文件系统访问等关键功能的内存错误
* **Fuchsia OS**：该操作系统内部代码有相当比例由Rust实现
* **Chromium**：已开始实验性支持Rust集成

**5. Dropbox**

* **同步引擎**：使用Rust替代原有的Python和C++代码，实现CPU使用率降低、并发性能提升和同步流程优化
* **核心文件存储系统**：多个核心组件采用Rust构建

**6. Discord**

* **后端服务**：在消息路由和在线状态追踪等关键后端服务中采用Rust，显著提升性能与可靠性。其“阅读状态”服务从Go迁移至Rust后有效避免了延迟峰值
* **客户端与服务器**：在客户端和服务器端代码库中均包含Rust组件

**7. Cloudflare**

* **Pingora**：用Rust开发的高性能网络代理，替代NGINX后实现了CPU使用率降低和连接管理优化
* **边缘核心逻辑**：使用Rust替代内存不安全的C语言等实现边缘计算核心逻辑
* **Cloudflare Workers**：支持使用Rust部署无服务器代码

**8. Mozilla**

* **Firefox（Stylo）**：作为Rust的原始创造者，使用该语言构建了Firefox的CSS引擎Stylo，显著提升性能与安全性
* **Servo**：完全基于Rust构建的实验性浏览器引擎

**9. npm（Node包管理器）**

* **认证服务**：使用Rust重写部分认证服务组件，实现安全性提升、负载处理能力增强和延迟降低

**其他重要采用者与项目：**

* **Linux内核**：Rust已成为Linux内核开发的第二官方语言，可用于开发更安全的设备驱动等模块
* **Figma**：将多人实时同步引擎从TypeScript重写为Rust以获得性能提升
* **1Password**：基于统一的Rust代码库构建最新桌面端与移动端应用
* **Hugging Face**：其AI生态系统中的`safetensors`、`tokenizer`和`candle`等多个组件均采用Rust实现
* **Polkadot**：为保障安全性与运行速度，该区块链平台完全基于Rust构建
* **Solana**：另一个充分利用Rust优势的高性能区块链平台
* **Brave浏览器**：在部分组件中采用Rust
* **Atlassian**：使用Rust开发用于分析PB级源代码的服务
* **华为**：在通信设备与基础设施工具领域已将部分代码库迁移至Rust

这些科技巨头对Rust的采用，充分证明了该语言在构建可靠、高效、安全的软件方面日益重要，特别是在系统级编程、基础设施和高性能应用领域。
