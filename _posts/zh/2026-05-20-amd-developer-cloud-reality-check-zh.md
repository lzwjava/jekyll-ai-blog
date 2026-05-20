---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD开发者云现实检验
translated: true
type: note
---

**问题：** 关于 AMD Developer Cloud 和 MI300X，有哪些小众或逆向观点？真实的开发者反馈如何？未来几个月的可用性预测是什么？

---

**答案：**

## AMD Developer Cloud — 未经修饰的真相

### 它到底是什么（AMD 轻描淡写的部分）

AMD Developer Cloud 实际上指向 DigitalOcean——本质上就是 DigitalOcean 的 GPU Droplets。因此“AMD Developer Cloud”这个品牌很大程度上是营销手段。你启动的是一个带有 devcloud.amd.com 包装的 DigitalOcean 实例。这一点会影响你对 SLA、网络和企业级功能的预期。

让 Phoronix 评测者感到意外的是：这些 AMD Developer Cloud 实例使用的是 Intel Xeon Platinum 8568Y+（Emerald Rapids）CPU——而不是 AMD EPYC。对于一个 AMD 用来推广自家芯片堆栈的云服务，搭载 Intel CPU 是一个值得注意的“自摆乌龙”。

---

### 逆向观点/小众看法

#### 1. CUDA 护城河真实存在，ROCm 并非即插即用的替代品

CUDA 领先 15 年，培养了 300 万熟悉 NVIDIA 编程模型的开发者、500 多个优化库，以及默认依赖 NVIDIA 硬件的框架。AMD 的 ROCm 通过 HIP 翻译承诺兼容 CUDA，但早期采用者报告称花费数月时间解决那些在 NVIDIA 系统上“开箱即用”的边缘情况。

对于 Transformer 模型性能至关重要的 Flash Attention，近期才获得 ROCm 支持，且运行速度比 CUDA 实现慢 20%。PyTorch 操作经常回退到较慢的通用实现，而非优化内核。

#### 2. AMD 自己的库大多是 CUDA 的衍生品

许多 AMD AI 库是 NVIDIA AI 库的分支，导致效果不佳和兼容性问题。AMD 客户通常只在推理时使用手工定制内核，这意味着在非常狭窄、定义明确的用例之外性能较差，并且面对快速变化的工作负载缺乏灵活性。

#### 3. 多节点训练是薄弱环节

由于 RCCL（ROCm 集体通信库）较弱，以及 AMD 在网络和交换硬件方面的垂直集成度低于 NVIDIA（后者紧密集成了 NCCL、InfiniBand/Spectrum-X），MI300X 无法提供强大的横向扩展性能。

Infinity Fabric 在 8-GPU 节点内表现不错，但 Infinity Fabric 仅能直接连接 8 个 GPU，而 NVLink 在 NVLink Switch 系统中可连接多达 256 个 GPU，这限制了 MI300X 只能用于较小集群，或在更大规模部署中依赖以太网/InfiniBand。

#### 4. “新硬件不可用”问题

AMD Developer Cloud 在 MI350X/MI355X 发布时同步上线，但并未提供任何 MI350 系列或 MI325X 的访问权限——仅有现有的 MI300X 和 ROCm 6.4.0（发布时已过时，6.4.1 已发布，ROCm 7.0 处于预览阶段）。

#### 5. 生态系统不成熟带来实际摩擦

历史上，AMD 的 OpenCL 实现通过了一致性测试，但性能糟糕。驱动程序漏洞百出。文档质量远不及 NVIDIA。产品不一致，开发者体验所有权不明确。约三周前（2026 年 5 月）的 HN 讨论表明，这种声誉至今仍在开发者圈子里困扰着 AMD。

AMD 要求开发者正确设置大量环境标志——多达数十个——才能使 AMD 部署可用。与直接运行 CUDA 相比，这是巨大的开发者体验税。

#### 6. 1.99 美元/GPU/小时在考虑摩擦后并不便宜

即使按 1.85 美元/小时（Vultr 的 MI300X 价格）计算，MI300X 也比 1.38 美元/小时的 H100 贵约 34%。除非你的模型确实需要 192GB 或 FP8，否则 1.38 美元/小时的 H100 通常能提供更好的 ROI。其价值主张仅适用于真正需要巨大显存的模型（70B+、长上下文、大批次）。

#### 7. 关机 ≠ 不计费

如果 GPU 实例处于关机状态，你仍然会被计费。只有在实例被销毁后才停止计费。对于习惯了 AWS 停止与终止语义的开发者来说，这是一个陷阱。一个周末忘记关闭闲置实例，就可能烧掉 100 美元额度。

---

### 真实世界的兼容性问题（近期）

截至 2025 年 8 月，LM Studio 的 ROCm 运行时在 AMD MI300X GPU Droplets（通过 DigitalOcean 的 Ubuntu 24.04）上被标记为“不兼容”。这类意外会浪费开发者一个下午。工具层面的差距真实存在。

---

### 可用性预测（未来约 6 个月，至 2026 年 11 月）

**简短答案：MI300X 仍可用但逐渐商品化。MI350X/MI355X 开始出现。**

截至 2026 年 4 月，MI300X 在 9 家云提供商处可用，包括 Vultr、TensorWave、Oracle、DigitalOcean、Crusoe、HotAisle、RunPod、Seeweb 和 Cirrascale。供应已不再是瓶颈。

按需定价自 2025 年 5 月以来上涨约 29%，从 2.35 美元/GPU/小时升至整个市场的 3.02 美元/GPU/小时——因此需求略超供应，但新云厂商正在激进压价。

方向性预测：
- **MI300X 在新云厂商处维持在约 1.85–2.20 美元/GPU/小时**，MI350X/MI355X 将占据高端市场。
- **AMD Developer Cloud 可能在 2026 年下半年添加 MI350X**，因为 MI355X 于 2025 年中发布并已开始出货。
- 随着 MI350X/MI355X 的推出，AMD MI300X 定价正在软化，一些新云厂商以低于 H100/H200 的美元/GPU/小时价格提供更多每 GPU 内存。
- ROCm 7.x 将成为默认堆栈（已处于预览阶段），修复了多个 PyTorch 兼容性问题。

---

### 支持 MI300X 的逆向案例

尽管存在上述问题——AMD 已通过 ROCm 6/7 跨过了可用性门槛：原生 PyTorch wheel、ROCm 容器以及 vLLM/SGLang 中的上游支持意味着如果你标准化使用 ROCm 镜像，开源堆栈可以“第 0 天”工作。

对于你的用例（70B+ 规模的 LLM 推理、长上下文、大批次），192GB 显存确实具有差异化优势。一张 MI300X 可以运行量化后的 DeepSeek-R1 671B，这需要 3 张以上 H100 80GB 卡。这正是使用它的真正原因。

**总结：** AMD Developer Cloud 是一个轻量化的 DigitalOcean 包装，搭载 Intel CPU、过时的 ROCm、没有更新的 AMD 芯片，并且生态系统仍需大量手动调优。1.99 美元/GPU/小时的价格在考虑与 H100 的 ROI 后并不便宜。其真正价值范围狭窄：如果你需要单 GPU 192GB+ 显存用于推理，或者需要测试 ROCm 兼容性以便进行开源贡献。对于大规模训练，CUDA 护城河依然稳固。

**参考来源：**

- [Phoronix: AMD Developer Cloud 评测](https://www.phoronix.com/review/amd-developer-cloud)
- [SemiAnalysis: MI300X vs H100/H200 基准测试第一部分——CUDA 护城河依然存在](https://newsletter.semianalysis.com/p/mi300x-vs-h100-vs-h200-benchmark-part-1-training)
- [getdeploying.com: MI300X 云定价 2026](https://getdeploying.com/gpus/amd-mi300x)
- [cloud-gpus.com: 2026 年 4 月 AMD GPU 提供商](https://cloud-gpus.com/amd-gpus/)
- [dstack: 2025 年云 GPU 现状](https://dstack.ai/blog/state-of-cloud-gpu-2025/)
- [Introl: AMD MI300X vs NVIDIA H100——坦诚分析](https://introl.com/blog/amd-mi300x-vs-nvidia-h100-breaking-cuda-monopoly)
- [HN: 为什么 AMD 的 MI300X 没有竞争力？](https://news.ycombinator.com/item?id=47929354)
- [LM Studio 漏洞：ROCm 在 DigitalOcean 上与 MI300X 不兼容](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/822)