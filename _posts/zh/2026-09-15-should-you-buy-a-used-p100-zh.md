---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 你应该购买二手P100吗？
translated: true
type: note
---

**问题：** 闲鱼上有人卖P100显卡，声称功能正常，计算负载稳定在240W，但需要自己解决散热问题——他们用风扇100%转速直吹。值得买吗？

**回答：**

从纸面上看，这笔交易还算合理，但有几个点需要了解：

**关于显卡本身**

NVIDIA Tesla P100（16GB HBM2）是数据中心GPU，没有板载散热——它专为有管理气流的服务器机箱设计。卖家提到风扇100%转速运行，这对于在机架环境之外使用该卡来说完全正常；这不是危险信号，而是在开放式环境中使用无风扇/涡轮散热服务器GPU的现实情况。

P100配备16 GB HBM2显存，带宽732 GB/s，FP32性能9.3 TFLOPS，TDP为250W。因此“稳定在240W”完全符合正常工况——这是预期行为，无需怀疑。

**价格现实**

二手P100在市场中很常见，通常价格在83–200美元之间，显存成本约5美元/GB——远低于T4或V100。目前最低平均跟踪价格在eBay等平台约为76美元。所以请比较闲鱼卖家的要价与这些基准。

**需要注意的事项**

- **散热由你负责。** 没有主动气流，这张卡会降频或损坏。你需要一个风扇直吹，或者安装在通风良好的机箱中。卖家100%转速风扇的做法是正确的。
- **PCIe vs SXM2接口**——确认是哪一种。SXM2版本需要专用中间板，而PCIe可插入标准主板。
- **供电**——250W TDP需要8-pin（或根据型号双8-pin）以及有冗余的电源。
- Pascal架构可能在一些较新的推理框架中软件支持有限——检查CUDA兼容性是否符合你的使用场景。
- **无显示输出**——这是一张纯计算卡。

**结论**

如果价格合理（约等于150美元以下）且卖家信誉可靠，这是一张不错的预算计算卡。他们给出的散热处理方案是合理且诚实的，这实际上是个好迹象。

---

参考来源：
- [NVIDIA Tesla P100 规格与价格 – GPUpoet](https://gpupoet.com/gpu/learn/card/nvidia-tesla-p100)
- [Tesla P100 二手价格与历史 – GPUDojo](https://gpudojo.com/tesla-p100)
- [P100 云价格与规格 – gpus.io](https://gpus.io/en/gpus/teslap100)
- [P100 AI/家庭实验室购买指南 – Alibaba Electronics](https://electronics.alibaba.com/product/nvidia-tesla-p100)