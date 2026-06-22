---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'OpenFold: 忠实复现的AlphaFold2'
translated: true
type: note
---

以下是OpenFold的介绍：

---

**OpenFold**——DeepMind **AlphaFold 2**（蛋白质结构预测）的忠实可训练PyTorch复现版本。

由哥伦比亚大学/哈佛大学的AlQuraishi实验室开发。该仓库拥有约159位贡献者，并持续维护中（近期有NVIDIA贡献支持cuEquivariance功能）。

**功能：** 输入蛋白质氨基酸序列，预测其三维原子结构。这是AlphaFold 2解决的同一难题——堪称人工智能在生物学领域最重大的突破。

**架构（基于代码）：**

`openfold/model/model.py`中的`AlphaFold`类实现了AlphaFold 2论文中的算法2，包含以下关键组件：

1. **输入嵌入器**（`embedders.py`）——将氨基酸序列+MSA（多序列比对）+模板嵌入为成对/表示张量。支持单体、多聚体以及"预嵌入"模式。

2. **进化模块**（`evoformer.py`，约1278行）——核心主干网络，包含多层堆叠：
   - MSA行/列注意力（含成对偏差、全局注意力选项）
   - 三角乘法（传出/传入）——存在融合CUDA变体
   - 三角注意力（起始/终止节点）
   - 外积均值（MSA→成对表示）
   - 成对过渡、MSA过渡
   - 梯度检查点+分块技术用于内存优化

3. **结构模块**（`structure_module.py`）——IPA（不变点注意力），从成对/表示张量生成三维原子坐标。采用SE(3)-等变运算。

4. **输出头**（`heads.py`）——辅助输出：pLDDT置信度、距离直方图、预测对齐误差（PAE）、掩码MSA。

5. **损失函数**（`utils/loss.py`）——FAPE（框架对齐点误差）、辅助距离/角度损失、pLDDT损失。

**训练：** `train_openfold.py`通过PyTorch Lightning模块（`OpenFoldWrapper`）封装，包含：
   - DeepSpeed ZeRO / DDP策略
   - 权重指数滑动平均（EMA）
   - AlphaFold专用学习率调度器
   - 多链排列对齐（用于多聚体）
   - WandB日志记录
   - 支持从JAX（原始DeepMind）和OpenFold检查点导入权重

**基础设施：**
   - `setup.py`中的CUDA扩展——针对注意力和三角运算的自定义内核
   - cuEquivariance集成（NVIDIA）
   - TensorRT推理支持（`utils/tensorrt_utils.py`）
   - 用于分布式训练的DeepSpeed集成
   - `openfold/data/`中的数据流水线——处理mmCIF、PDB、MSA生成
   - Amber弛豫（`np/relax/`）——基于物理的能量最小化预测结构

**关键文件：**
   - `openfold/config.py`——模型配置（单体、多聚体、不同规模）
   - `openfold/model/`——所有神经网络模块（15个文件）
   - `openfold/utils/`——损失函数、几何运算（SO(3)/SE(3)）、权重导入、检查点
   - `openfold/data/`——数据加载、转换、比对预处理
   - `scripts/`——用于比对、嵌入、数据缓存的预处理脚本

这是一个庞大的机器学习代码库（约5万行以上），实现了生产环境中最为复杂的AI架构之一。近期提交聚焦于NVIDIA优化（三角运算的cuEquivariance支持、TRT推理）。