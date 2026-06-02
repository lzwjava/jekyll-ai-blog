---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 芯折射率高于包层
translated: true
type: note
---

**问题：** 光纤由 core 和 cladding 组成。core 的折射率是 ________ cladding 的折射率。

**答案：**

## 答案： **大于**

core 的折射率**大于** cladding 的折射率。

---

### 全面解释

#### 1. 光纤的基本结构

光纤有两个主要层：

| 层   | 作用               | 折射率         |
|------|--------------------|----------------|
| **Core (纤芯)** | 携带/引导光信号     | **更高 (n₁)** |
| **Cladding (包层)** | 将光限制在 core 内 | **更低 (n₂)** |

因此关系是：**n₁ (core) > n₂ (cladding)**

---

#### 2. 为什么 core 必须具有更高的折射率？

光纤的整个工作原理基于 **Total Internal Reflection (全内反射, TIR)**：

- 为了将光学信号限制在 core 中，core 的折射率必须大于 cladding 的折射率。
- cladding 通过 core 和 cladding 边界处的 total internal reflection 将光限制在光纤的 core 中。

Total Internal Reflection 仅当光从**较稠密介质（较高 n）传播到较稀疏介质（较低 n）**且入射角超过**critical angle**时发生。这正是发生在 core-cladding 边界处的情况。

---

#### 3. Total Internal Reflection 在光纤中如何工作

- 光进入 **core**（高折射率 n₁）。
- 光以陡峭角度（大于临界角）击中 **core-cladding 边界**。
- 注入光纤 core 并以大于临界角的角度击中 core-to-cladding 接口的光被反射回 core。由于入射角和反射角相等，光线继续沿光纤长度呈锯齿状前进。光被困在 core 内。
- 如果角度太小（小于临界角），光会进入 cladding 并**丢失**。

---

#### 4. 折射率值的真实世界示例

典型的用于电信的 single-mode fiber，其 cladding 由纯 silica 制成，在 1500 nm 处的折射率为 1.444，core 为掺杂 silica，折射率约为 1.4475。

这表明差异很小但至关重要——core 的折射率总是略高于 cladding。

---

#### 5. 临界角公式

临界角 θ_c 由以下公式确定：

$$\sin\theta_c = \frac{n_2}{n_1}$$

其中 n₁ 是 core 的折射率，n₂ 是 cladding 的折射率。core 的折射率 n₁ 总是大于 cladding 的折射率 n₂。光通过 core 引导，光纤充当 optical waveguide。

---

#### 总结

> core 的折射率**大于** cladding 的折射率。这个差异是实现 total internal reflection 的物理基础，这就是光纤以最小损耗在长距离上引导光的方式。

**参考文献：**

- [Optical fiber - Wikipedia](https://en.wikipedia.org/wiki/Optical_fiber)
- [Cladding (fiber optics) - Wikipedia](https://en.wikipedia.org/wiki/Cladding_(fiber_optics))
- [The Physics Behind Fiber Optics - Cisco Press](https://www.ciscopress.com/articles/article.asp?p=170740&seqNum=3)
- [Fiber Core - RP Photonics](https://www.rp-photonics.com/fiber_core.html)
