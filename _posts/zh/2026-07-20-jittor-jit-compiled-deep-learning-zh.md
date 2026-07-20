---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Jittor: 即时编译的深度学习'
translated: true
type: note
---

问题：什么是Jittor（github.com/Jittor/jittor）？

回答：Jittor是清华大学计算机系图形学与几何计算课题组（CSCG）推出的深度学习框架，其与PyTorch/TensorFlow的核心区别在于**整个框架在运行时进行即时编译（JIT），而不仅仅是算子层面**。

核心理念：
- 采用Python前端与动态图（命令式风格，类似PyTorch的`nn.Module`/autograd模式），但每个算子调用都会实时生成并编译C++/CUDA代码并进行缓存。
- **元算子**：无需手工编写每个融合内核（如卷积、池化等），而是定义一组基础元算子，它们会被组合并通过JIT融合为针对特定形状、数据类型和设备的专用内核。官方声称：这种方法无需为每种算子组合编写CUDA即可接近手工优化的CUDA性能。
- 统一的算子计算图（而非PyTorch的即时逐算子调度模式），因此编译器能够在运行前跨多个算子进行融合和优化。

API层面与PyTorch高度相似：

```python
import jittor as jt
from jittor import Module, nn

class Model(Module):
    def __init__(self):
        self.layer1 = nn.Linear(1, 10)
        self.relu = nn.Relu()
        self.layer2 = nn.Linear(10, 1)
    def execute(self, x):   # forward() -> execute()
        x = self.layer1(x)
        x = self.relu(x)
        return self.layer2(x)

model = Model()
optim = nn.SGD(model.parameters(), 0.1)
jt.flags.use_cuda = 1
```

值得注意的点：
- 使用`execute()`替代`forward()`。
- 使用`Var`替代`Tensor`，计算是异步的——`.data`用于强制同步。
- 自定义算子：使用C++/CUDA编写算子，通过JIT内联编译，无需像PyTorch扩展那样执行独立的`setup.py build_ext`步骤。
- 后端支持：g++/clang++，兼容CUDA >=10、AMD ROCm >=4.0，以及海光DCU（国产GPU）。
- 采用Apache 2.0许可证，拥有约3200颗星，维护活跃（最新版本1.3.10.0），代码占比Python 54% / C++ 39%。

适用场景：主要应用于中国学术界的计算机视觉/图形学研究（明确提及可微渲染、几何学习等领域）——相比PyTorch/JAX属于小众框架，但其JIT元算子设计为`torch.compile`/XLA融合提供了一种可行的替代方案，适合深入探索编译器层面的深度学习框架设计。

参考信息：
- [Jittor/jittor](https://github.com/Jittor/jittor)
- [Jittor网站](https://cg.cs.tsinghua.edu.cn/jittor/)