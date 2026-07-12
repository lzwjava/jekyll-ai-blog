---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 希捷5TB Backup Plus外置硬盘
translated: true
type: note
---

问题：希捷 Backup Plus 5TB 便携式外置硬盘 USB 3.0，黑色 简介

答案：

希捷 Backup Plus 5TB 便携式硬盘是一款主要面向**备份、归档以及移动大文件**的 **2.5 英寸外置机械硬盘 (HDD)**。它不是固态硬盘 (SSD)，内部采用传统的旋转式磁盘。([Seagate.com][1])

### [希捷 Backup Plus 便携式 5TB 外置硬盘 USB 3.0 黑色](https://www.walmart.com/ip/Seagate-5TB-Backup-Plus-External-Portable-Drive-USB-3-0-BLACK/677085372?utm_medium=feed&utm_source=chatgpt.com)

*$189.00 美元*

## 主要规格

* 容量：**5TB**
* 接口：**USB 3.0**（向下兼容 USB 2.0）
* 外形规格：**2.5 英寸便携式机械硬盘 (HDD)**
* 供电：USB 总线供电（无需外接电源适配器）
* 重量：约 **247–265 克**
* 尺寸：约 **115 × 80 × 21 毫米**
* 保修：通常为 **2 年有限保修**，具体视地区/型号而定 ([Seagate.com][1])

## 内部构造

基本结构如下：

```
计算机
   |
 USB 3.0 数据线
   |
[ USB 转 SATA 桥接芯片 ]
   |
[ 2.5 英寸希捷机械硬盘 ]
   |
[ 磁盘盘片 + 磁头臂 ]
```

它类似于笔记本电脑内部的硬盘，但被安置在一个 USB 外置盒中。

典型实际性能：

```
顺序读写：
约 100-150 MB/s（有时更高）

随机读写：
约 1-10 MB/s
```

与固态硬盘 (SSD) 对比：

```
                 机械硬盘 (HDD)    固态硬盘 (SSD)
每GB容量价格       ★★★★★            ★★★
速度              ★★               ★★★★★
抗震性            ★★               ★★★★★
长期归档存储      ★★★★             ★★★
噪音              有               无
```

## 适用场景

### 1. 备份

适合备份：

* 照片
* 视频
* 文档
* 源代码归档
* 机器学习数据集
* 模型检查点

示例：

```
笔记本电脑 固态硬盘 1TB
       |
       v
希捷 5TB 备份

~/projects
~/datasets
~/models
~/photos
```

对于你的 AI 工作，它可以存储：

* HuggingFace 数据集
* 模型权重
* 训练日志
* Docker 镜像
* 检查点

示例：

```
datasets/
 ├── FineWeb/
 │    └── 100B tokens
 ├── SEC-EDGAR/
 └── custom_corpus/

models/
 ├── gpt2-124m/
 ├── llama/
 └── checkpoints/
```

## 局限性

### 1. 不适合直接用于训练

对于 PyTorch 训练：

不推荐：

```
GPU
 |
PCIe
 |
内存
 |
USB 机械硬盘  ← 瓶颈
```

推荐：

```
GPU
 |
PCIe
 |
NVMe 固态硬盘
```

如果可能，训练数据集应放在 NVMe 固态硬盘上。

将此机械硬盘用于：

```
冷存储
↓
备份
↓
归档
```

### 2. 机械故障风险

硬盘包含运动部件：

* 主轴电机
* 磁头臂
* 磁盘盘片

运行时跌落可能使其损坏。

原则：

```
重要数据：
1 份拷贝 = 有数据风险
2 份拷贝 = 较为安全
3 份拷贝 = 专业级别
```

示例：

```
本地 NVMe 固态硬盘
      +
希捷 5TB 机械硬盘
      +
云端备份
```

## 希捷 Backup Plus 与其他希捷型号对比

希捷有多款便携式机械硬盘产品线：

```
Backup Plus
    |
    +-- 更精致的外壳
    +-- 附带备份软件
    +-- 消费级高端型号

Expansion Portable
    |
    +-- 价格更低
    +-- 基础存储功能

One Touch
    |
    +-- 较新的高端型号
    +-- 加密/附加功能
```

许多用户反映，希捷不同便携式产品线内部往往使用相似的机械硬盘；主要区别在于外壳、软件和功能。([Reddit][2])

## 针对你的使用场景

考虑到你的工作涉及：

* 大型语言模型 (LLM) 训练实验
* 数据集
* GPU 机器
* 大量代码/检查点

一个理想的存储架构：

```
PC 电脑
 |
 +-- 1TB/2TB NVMe 固态硬盘
 |       |
 |       +-- 活跃训练任务
 |
 +-- 希捷 5TB 机械硬盘
         |
         +-- 数据集归档
         +-- 检查点
         +-- 备份
```

这款硬盘是一个**廉价的大容量存储层**，而非性能层。

对于 AI 开发，大致优先级排序：

```
1. NVMe 固态硬盘  ⭐⭐⭐⭐⭐
2. 内存 (RAM)    ⭐⭐⭐⭐⭐
3. 显存 (GPU VRAM) ⭐⭐⭐⭐⭐
4. 外置机械硬盘    ⭐⭐⭐
```

参考资料：

* 希捷 Backup Plus 便携式硬盘规格 ([Seagate.com][1])
* 希捷 Backup Plus 5TB 产品页面

[1]: https://www.seagate.com/support/external-hard-drives/portable-hard-drives/backup-plus/?q=STDR1000200&utm_source=chatgpt.com "Backup Plus 便携式硬盘支持页面 | Seagate US"
[2]: https://www.reddit.com/r/DataHoarder/comments/opmod3/is_the_seagate_one_touch_5tb_a_good_or_at_least_a/?utm_source=chatgpt.com "希捷 One Touch 5TB 是一款好（或至少合格）的硬盘吗？"