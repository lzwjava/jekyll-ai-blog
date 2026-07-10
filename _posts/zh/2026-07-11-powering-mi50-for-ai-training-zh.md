---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 驱动MI50进行AI训练
translated: true
type: note
---

问题：海盗船CX650F / 750W电源能否为AMD Radeon Instinct MI50 16GB提供AI训练所需的电力？

答案：

是的，**海盗船CX650F 650W**或**750W 80+电源**可以为AMD MI50供电，但有几个重要细节需要注意。

AMD Radeon Instinct MI50功耗要求：

* **TDP：** ~300W
* **电源接口：** **1个8针PCIe电源接口 + 1个6针PCIe电源接口**（与RTX 4070不同）
* **推荐电源：** 通常为650W以上，具体取决于系统其他部件

MI50是一款数据中心显卡，因此不使用RTX 40系列的新款12VHPWR接口。

您的电源：

海盗船CX650F RGB

或750W版本：

* PCIe 8针线缆：有
* 功率足够：是
* 质量：对于单张MI50来说可以接受

典型系统：

```
CPU（Ryzen 7 / Intel i7）     80-150W
主板 + 内存                  50W
SSD + 风扇                  20W
AMD MI50                    ~300W
----------------------------------
总计                       ~450-520W
```

因此，一款优质的650W电源有足够的余量。

不过，请检查**PCIe电源线**：

MI50需要：

```
PSU PCIe线缆
       |
       +---- 8针 PCIe -> MI50
       |
       +---- 6针 PCIe -> MI50
```

**不要**使用：

```
SATA转PCIe转接头  ❌
Molex转PCIe转接头 ❌
```

因为该显卡在AI负载下持续功耗接近300W。

---

您的闲鱼MI50商品信息：

> 16G HBM2 ECC，性能与RTX 3060类似，AI训练，温度90°C

描述基本合理，但有一些说明：

### 性能

MI50：

* 16GB HBM2 ECC
* 10240个流处理器
* ~13.3 TFLOPS FP32
* ~1TB/s内存带宽

与RTX 3060对比：

| GPU           | VRAM          | 内存带宽      | FP32        |
| ------------- | ------------- | -------------- | ----------- |
| RTX 3060 12GB | GDDR6 12GB    | 360 GB/s       | 12.7 TFLOPS |
| MI50          | HBM2 16GB ECC | ~1 TB/s        | 13.3 TFLOPS |

对于**大型模型推理/训练**，MI50实际上感觉更好，因为：

* 16GB VRAM
* 巨大带宽
* ECC
* 二手价格便宜

但软件是问题所在：

* CUDA生态 ❌
* PyTorch ROCm支持 ⚠️
* 许多AI软件包默认支持NVIDIA

您需要使用兼容ROCm的版本。

---

以630元的价格，MI50很有吸引力：

```
RTX 4070：
12GB GDDR6X
CUDA
~200W

MI50：
16GB HBM2 ECC
~300W
ROCm
```

对于您的使用场景（本地LLM实验），最大的优势是：

**16GB VRAM + ECC，仅630元，非常便宜。**

购买前我建议验证以下内容：

```bash
lspci | grep VGA
rocm-smi
python -c "import torch; print(torch.cuda.is_available())"
```

安装ROCm后执行。

同时检查散热。MI50显卡通常运行温度较高，因为它们是为服务器风道设计的。机箱风道不好的台式机很容易达到90°C。对于长时间训练，请增加强劲的侧吹/前吹风扇或使用涡轮散热方案。