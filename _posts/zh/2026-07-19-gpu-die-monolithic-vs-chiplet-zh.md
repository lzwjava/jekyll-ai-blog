---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU芯片：单片式与芯粒式
translated: true
type: note
---

问题：什么是GPU芯片（die）？

答案：芯片（die）是从晶圆上切割下来的实际硅片，包含已制造好的电路——即封装前的物理芯片。“GPU芯片”指的是实现GPU计算单元（NVIDIA上的SM，AMD上的CU）、内存控制器、L2缓存以及互联架构的硅片。

关键机制：

**晶圆 → 芯片**
- 晶圆厂在约300mm的硅晶圆上刻印数千个设计副本，然后切割（dicing）成单个芯片
- 芯片尺寸受光掩模限制（当前EUV光刻最大约858mm²）——这就是为什么大型GPU芯片（H100约814mm²，MI300X计算芯片因小芯片设计而更小）会逼近这一上限
- 芯片越大 = 每片晶圆产出的芯片数量越少 + 良率越低（缺陷概率随面积增加） = 每颗合格芯片成本更高

**单片式 vs 小芯片**
- 单片式：单个大芯片完成所有功能（旧款GPU，NVIDIA H100/B200计算芯片仍采用此设计）
- 小芯片：通过中介层/封装连接多个小芯片（AMD MI300X正是如此——它包含XCD（计算芯片，CDNA3架构）+ IOD（输入/输出芯片）+ HBM堆叠，全部通过CoWoS封装技术融合）
- MI300X具体配置：8个XCD小芯片 + 4个IOD小芯片 + 8个HBM3堆叠，整个封装共约1530亿晶体管——没有单个芯片能独立实现这一切

**这对你在MI300X上训练的重要性**
- 跨XCD通信（Infinity Fabric）与芯片内通信具有不同的带宽/延迟——这会影响训练框架应如何放置张量并行分片。如果你正在手动调整NCCL/RCCL，芯片拓扑结构正是同一物理封装上某些GPU对比其他更“近”的原因。
- 芯片良率的经济性也是AMD/NVIDIA对大型芯片零件（H100、MI300X）定高价的原因——次品芯片会被降级为精简版SKU（例如，减少活跃的SM/CU数量）。

**快速检查**：运行以下命令查看MI300X实际的芯片/封装拓扑结构：
```bash
rocm-smi --showtopo
```
或对于NVIDIA：
```bash
nvidia-smi topo -m
```

参考文献：
- [AMD Instinct MI300X数据表](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)
- [小芯片架构——AMD CDNA3白皮书](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/white-papers/amd-cdna-3-white-paper.pdf)
- [光掩模限制解释——SemiAnalysis](https://semianalysis.com/)