---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 预算Vega 20集群用于训练
translated: true
type: note
---

**问题：** 用约6000元人民币组建一个包含10块AMD Radeon Pro VII（每块16GB，约600元，卖家将其误标为MI50出售）的集群，对于本地训练来说是否值得？10块显卡能否扩展到100块？

**答案：**

**“误标”的说法属实。** Radeon Pro VII和MI50本质上是相同的Vega 20核心，主要区别在于品牌、固件和物理封装——MI50禁用了显示输出并移除了被动散热，而Pro VII保留了mini-DisplayPort 1.4a输出和主动散热。闲鱼/转转上的卖家经常给MI50显卡刷上Pro VII的VBIOS（反之亦然），因为两者在电气上完全相同。在计算性能上你并没有被骗——只是标签上被忽悠了，而且卖家甚至卖便宜了。让他继续卖吧。

**ROCm状态——这才是真正的限制，而非PCIe。** gfx906 GPU（MI50、Radeon Pro VII、Radeon VII）在ROCm 6.0中进入了维护模式。ROCm 5.7是gfx906最后一个获得完全支持的正式版本。实际操作上：

```bash
# 最后为gfx906官方构建的ROCm（含供应商二进制文件）：5.7
# 此后，你需要自行编译或使用社区构建：
# mi50可与ROCm 6.4.3配合使用，但需使用Arch的rocblas中的一个小型rocblas包补丁
# https://github.com/nlzy/vllm-gfx906 是用于推理的主流社区分支
```

MI50在代码层面仍有良好支持，但AMD不再为其构建二进制文件。你需要自行编译支持gfx906的ROCm，或使用社区维护的软件包。因此：推理（vLLM分支，llama.cpp配合HIP后端）——没问题。在最新ROCm上使用完整的PyTorch+ROCm+RCCL栈进行训练——预计会出现问题，建议锁定到5.7版本或使用社区的6.4.3补丁。

**10块显卡的PCIe扩展——不要使用矿卡转接卡。** 对于实际的训练（每一步都需要梯度全规约），x1的矿卡转接卡（250MB/s）会严重瓶颈化。真正的选择，从最廉价到性能最强：

```bash
# 选项1：具备真实通道数的二手服务器主板（最具价值）
# AMD EPYC Rome/Milan (SP3) — 单路提供128条PCIe4通道，单路足够
# 例如：二手超微H11/H12主板，二手价约1500-3000元
# 无需交换机即可提供6-8个真正的x8/x16插槽

# 选项2：如果你只能使用消费级主板，考虑PCIe分叉+重定时器
# x16插槽 -> 通过分叉转接卡变为4个x4（需要BIOS支持分叉）
# 检查：lspci -vvv | grep -i "LnkCap\|LnkSta"  # 安装后验证协商的带宽/速度

# 选项3：如果不支持分叉，使用PCIe交换卡（基于ASM2824，从一个x8扩展出4个x4）
```

组装后检查RCCL/P2P支持：
```bash
rocminfo | grep -A5 "Pool Info"
rocm-smi --showtopo   # 显示GPU间的P2P链路矩阵
```
gfx906**不支持**像MI50通过xGMI桥接卡配对那样实现PCIe P2P——在没有相邻配对之间的xGMI桥接卡时，所有规约流量走GPU→CPU→GPU路径通过PCIe，这才是你实际训练中的瓶颈，而不是转接卡本身。

**成本计算是真实的，但并非同类比较：**

|                | Pro VII（10块）       | A6000 Pro         |
| -------------- | -------------------- | ----------------- |
| 显存            | 160GB                | 96GB              |
| 成本            | 约6000元              | 约5-6万元          |
| FP16           | 约26.8 TFLOPS/卡，总计268 | 更高密度，单卡更高 |
| 每卡带宽        | 1.02 TB/s HBM2       | 约960GB/s GDDR6   |
| 互连            | 仅PCIe，无NVLink      | 仅PCIe（Pro同样无NVLink，非Ada版A6000） |
| 软件风险        | 高（ROCm EOL，需自行构建）| 低（CUDA，当前主流）|
| 功耗            | 300W x10 = 3kW       | 300W x1           |

每元显存比对你有利约15倍，但这忽略了软件栈的维护时间（对于你运营一家AI公司来说，这不是免费的），以及当GPU数量超过2-4块时在纯PCIe环境下的全规约瓶颈。这个方案真正胜出的场景是：**大批量推理/服务，或对中小型模型进行数据并行微调（每个GPU持有完整副本，极易并行，最小化同步）**——而不是跨全部10块GPU对单个大型模型进行张量并行训练。

**关于“10块显卡解决了，100块也不远了”：** 需要反驳这一点。从10块到100块不是简单的乘法，而是一个不同的问题——功耗（30kW+，需要三相电）、机架/冷却、网络架构（如果需要真正的多节点吞吐，需要RDMA/RoCE），以及ROCm对gfx906的EOL意味着在这个规模下你需要维护自己的分支，这是一个实打实且持续的成本。如果实际目标是“廉价本地训练能力”，一台配备4-8块拥有真正NVLink或优质PCIe4 x16通道的二手A100/A6000节点，在算上工程时间后，每元人民币能为你带来的可用训练吞吐量将超过10块Pro VII。Pro VII集群作为推理/实验平台，或用于需要大量并行小模型实例的RL/agent大规模部署工作负载是有意义的，但绝非一个密集的预训练集群。

参考文献：
- [Radeon VII vs MI50 品牌标识](https://www.aliexpress.com/s/wiki-ssr/article/radeon-vii-vs-mi50)
- [ROCm 6.0 gfx906 维护模式](https://rocm.docs.amd.com/en/docs-6.0.0/about/release-notes.html)
- [ROCm 5.7 发行说明 — gfx906 EOS](https://rocm.docs.amd.com/en/docs-5.7.0/release.html)
- [社区 gfx906 ROCm 6.4.3 工作区讨论](https://github.com/ROCm/ROCm/discussions/4276)
- [vllm-gfx906 分支](https://github.com/nlzy/vllm-gfx906)