---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD DevCloud 指南与限额提升
translated: true
type: note
---

**问题：** AMD 开发者云（devcloud.amd.com）如何运作？如何提升 Droplet 限制？

---

## AMD 开发者云 — 运作方式

关键架构事实：**devcloud.amd.com 底层基于 DigitalOcean。** AMD 开发者云依赖 DigitalOcean 提供云环境，并最终部署 GPU Droplet。您可以创建单 GPU 或 8 路 AMD Instinct MI300X 实例。AMD 本质上是以转售商/合作伙伴的身份在 DO 的 GPU 基础设施上提供一层封装。

### 您将获得什么

它通过预装流行 AI 软件的 Docker 容器提供对 AMD GPU 的便捷访问，最大限度减少设置时间，同时让开发者灵活地定制代码。Jupyter Notebook 环境在容器内运行，并在虚拟机启动时可用——无需本地设置。

硬件方面：MI300X 配备 192GB HBM3 内存，使得在单实例上运行 70B+ 参数模型而无需模型并行成为可能。

### 访问与积分

如需申请，请访问 devcloud.amd.com 创建账户或登录，填写“申请积分”表单。若获批，初始 25 小时云积分将添加至您的账户。

积分分配由 AMD 根据预期使用场景（推理、训练、微调）以及您计划如何使用 GPU 积分的详细描述来决定。您也可以添加支付选项并即用即付，或随时切换至生产云。

关键注意事项：如果 GPU 实例处于关闭状态，您仍会被计费，且积分时间仍会计入。费用将持续产生，直至实例被销毁。

### 虚拟机配置选项

用户可以从零开始配置带有自己偏好的 AI/ML 软件的虚拟机，选择预装主流框架（PyTorch、vLLM 等）Docker 镜像的虚拟机，或直接启动至虚拟机创建时即提供的现成 JupyterLab 环境。

---

## 提升 Droplet 限制

由于 AMD 开发者云基于 DigitalOcean，Droplet 限制（默认 10 个）通过 DO 控制面板进行管理。

**步骤：**

在 DigitalOcean 控制面板左侧菜单中，点击 **资源限制**。然后点击右上角的 **请求提升**。在下拉菜单中选择资源（Droplet 或 GPU Droplet），输入新的限制值，并在“原因”字段中描述您的使用场景。点击提交。

**在原因字段中应写明的内容**——请具体说明。根据社区报告：批准与否取决于您对使用场景和预期工作负载的说明，并可能取决于您当前的方案和使用历史。

对于 GPU Droplet 而言：要创建多节点 GPU Droplet，您需要联系技术支持以在您的团队中启用该功能——仅凭控制面板是不够的。

**直接联系 AMD** 处理积分/访问问题：`devcloudrequests@amd.com`

---

## 针对您使用场景的实用说明

- MI300X + ROCm 堆栈是主要价值所在——这是在不拥有硬件的情况下测试 ROCm 原生代码（HIP、rocBLAS、hipBLAS）的唯一途径。
- 25 小时免费时间足以进行一次快速微调运行（在 7B 模型上运行 LoRA 在 192GB 内存中绰绰有余）。
- **完成后销毁实例**——空闲计费是一个真正的陷阱。
- 如果您在对比 PyTorch ROCm 与 CUDA 的性能，这是无需购买 MI300X 硬件的最便宜合法途径。

参考资料：

- [AMD 开发者云 — 如何开始使用](https://www.amd.com/en/developer/resources/technical-articles/2025/how-to-get-started-on-the-amd-developer-cloud-.html)
- [AMD 云访问与积分计划](https://www.amd.com/en/developer/resources/cloud-access.html)
- [Phoronix 评测 — DigitalOcean 上的 AMD 开发者云](https://www.phoronix.com/review/amd-developer-cloud)
- [DigitalOcean — 查看和请求资源限制](https://docs.digitalocean.com/platform/teams/how-to/view-resource-limits/)
- [DigitalOcean Droplet 限制文档](https://docs.digitalocean.com/products/droplets/details/limits/)
