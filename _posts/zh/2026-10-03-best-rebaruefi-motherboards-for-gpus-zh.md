---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 最佳支持ReBar UEFI的GPU主板
translated: true
type: note
---

问题：ReBarUEFI 中哪些主板是 4G 解码 + CSM 配置的好选择？

回答：

针对你的使用场景（AI GPU 实验室，RTX 3090/4090/P100/M40 实验，大显存 BAR，多 GPU），我会优先考虑以下主板：

1. 拥有 **UEFI BIOS**
2. 提供 **Above 4G Decoding** 选项
3. 可以禁用 **CSM**
4. 具备足够的 PCIe 资源
5. 有已知的 ReBarUEFI 成功案例

ReBarUEFI 需要（或强烈建议）**启用 4G 解码并禁用 CSM**。如果没有 4G 解码，BAR 大小会受到限制。([GitHub][1])

从测试列表中，我推荐以下几款：

| 主板                           | 平台             | ReBarUEFI 结果                    | 我的评价                      |
| ------------------------------ | ---------------- | --------------------------------- | ----------------------------- |
| **ASUS Z170-A**                | Z170 / i7-6700   | RTX 3080/3090, 8-16GB BAR 已测试  | ⭐⭐⭐⭐⭐ 最佳廉价选择            |
| **ASUS Z170-P**                | Z170 / 6 代      | RTX 3090 32GB BAR 已测试          | ⭐⭐⭐⭐⭐ 非常优秀                |
| **ASUS Z170-WS**               | Z170 工作站      | Arc A770 16GB                     | ⭐⭐⭐⭐⭐ 最佳 Z170               |
| **MSI Z170-A PRO**             | Z170             | RX 6650 XT                        | ⭐⭐⭐⭐ 良好                     |
| **MSI Z170 KRAIT GAMING**      | Z170             | RX 6900 XT                        | ⭐⭐⭐⭐ 良好                     |
| **ASUS Z270-A Prime**          | Z270             | RTX 3060 Ti                       | ⭐⭐⭐⭐⭐ BIOS 更好               |
| **MSI Z270 GAMING M5**         | Z270             | RTX 3080 Ti                       | ⭐⭐⭐⭐ 良好                     |
| **ASUS X99-A / X99-DELUXE II** | X99              | RTX 3090/A6000 16-24GB            | ⭐⭐⭐⭐⭐ 最佳多 GPU              |
| **华南金牌 X99-QD4**           | X99              | RTX 3060 16GB                     | ⭐⭐⭐⭐ 廉价国产选项             |

([GitHub][2])

根据你之前对 Z170 的搜索，我的排名如下：

### 1. ASUS Z170-A

很可能是最佳选择。

原因：

* 闲鱼上便宜
* 支持 Intel 6 代
* DDR4
* M.2
* ASUS BIOS 好用
* 已知 ReBarUEFI 成功案例
* 有 Above 4G Decoding 选项

典型配置：

```
ASUS Z170-A
+
i7-6700 / i7-6700K
+
32GB DDR4
+
RTX 3090 24GB
```

BIOS 修改后可能暴露大 BAR。([GitHub][2])

### 2. ASUS Z170-P

同样优秀。

ReBarUEFI 列表中明确有：

```
ASUS Z170-P
RTX 3090
32GB BAR
```

这与你的 GPU 实验非常相关。([GitHub][2])

缺点：

* PCIe 插槽较少
* 工作站特性较弱

### 3. X99 主板

针对你的 AI GPU 方向，X99 实际上更有趣。

示例：

```
X99
+
E5-2680 v4
+
64GB DDR4 ECC
+
Tesla / RTX 显卡
```

ReBarUEFI 列表中有 X99 主板与 RTX 3090、RTX A6000 等配合工作的案例。([GitHub][2])

优势：

* 更多 PCIe 通道
* ECC 内存
* 廉价的 Xeon 处理器

缺点：

* BIOS 质量参差不齐
* 国产主板需要更多调试

避免：

### 旧款 Z97 / Haswell（除非非常便宜）

许多 Haswell 系统缺少 4G 解码选项，导致难以实现大 BAR。([GitHub][3])

### ASRock Z170 K4/D3

已知问题：

* 启用 4G 解码后 SATA 控制器出现故障。([GitHub][3])

根据你当前的目标（维修 + AI GPU 实验室），我的购买顺序是：

```
1. ASUS Z170-A        ~250-350 元
2. ASUS Z170-P        ~250-300 元
3. ASUS Z170-WS       如果便宜
4. X99 + E5 v4        用于多 GPU
5. MSI Z170/Z270      如果非常便宜
```

另外，在闲鱼上查看列表时，请搜索 BIOS 截图中的以下选项：

```
Above 4G Decoding
CSM Support
Launch CSM
PCI Subsystem Settings
```

对于这类 BIOS 修改工作，ASUS BIOS 通常比 MSI 更方便。

我还可以为你制作一份 **专门用于 500 元以下、多 GPU AI 实验室（RTX 3090/M40/P100）的闲鱼主板短名单**。

[1]: https://github.com/xCuri0/ReBarUEFI?utm_source=chatgpt.com "GitHub - xCuri0/ReBarUEFI: Resizable BAR for (almost) any UEFI system · GitHub"
[2]: https://github.com/xCuri0/ReBarUEFI/wiki?utm_source=chatgpt.com "Home · xCuri0/ReBarUEFI Wiki · GitHub"
[3]: https://github.com/xCuri0/ReBarUEFI/wiki/Common-issues-%28and-fixes%29?utm_source=chatgpt.com "Common issues (and fixes) · xCuri0/ReBarUEFI Wiki · GitHub"
