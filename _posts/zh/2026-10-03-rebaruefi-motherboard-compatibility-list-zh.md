---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ReBarUEFI 主板兼容性列表
translated: true
type: note
---

问题：在 `xCuri0/ReBarUEFI` 中，我可以在哪里找到哪些主板支持 4G 解码 / CSM / 相关的 BIOS 情况？

答案：

您想要的页面是 **Wiki → 已测试主板列表**：

[xCuri0/ReBarUEFI Wiki - 已测试主板列表](https://github.com/xCuri0/ReBarUEFI/wiki?utm_source=chatgpt.com)

在该表格中，查看：

* **主板**
* **UEFIPatch 需求 (是/否)**
* **备注**
* 测试的 GPU
* 实现的 BAR 大小

示例：

```
主板                      UEFIPatch   备注
---------------------------------------------------------
ASUS Z170-A               Y           ...
Huananzhi X99-QD4         N           ...
MSI B150M PRO-VDH         N           ...
ASUS Z170-P               Y           RTX3090 32GB BAR
```

该表格**并不总是直接说明“具有 4G 解码选项”**，因为许多主板隐藏了该选项。相关页面为：

[xCuri0/ReBarUEFI - 启用隐藏的 4G 解码](https://github.com/xCuri0/ReBarUEFI/wiki/Enabling-hidden-4G-decoding?utm_source=chatgpt.com)

该页面解释了如何查找隐藏的 BIOS 变量：

使用 UEFITool 搜索 BIOS：

```
4G Decod
Above 4G
MMIO
64-Bit Resource Allocation
```

如果找到，您可以使用 `setup_var` 启用它。（[GitHub][1]）

关于 CSM：

通常规则为：

```
4G 解码 = 启用
CSM = 禁用
仅 UEFI 启动
```

ReBarUEFI README 明确指出，安装修改后的固件后：

```
确保 4G 解码已启用，并且 CSM 已关闭
```

（[GitHub][2]）

针对您的情况：

### Z170 / B150 / X99

良好的候选主板：

* ASUS Z170-A
* ASUS Z170-P
* MSI Z170A 系列
* Huananzhi X99-QD4
* Huananzhi X99-TF
* ASUS X99 系列

它们已有成功报告。（[GitHub][3]）

### 购买二手主板时

请查看这些页面：

1. 谷歌搜索：

```
<主板型号> "Above 4G Decoding"
```

2. 搜索 BIOS 手册：

```
<型号> manual pdf "Above 4G"
<型号> manual pdf "CSM"
<型号> manual pdf "PCI Subsystem Settings"
```

3. 搜索 ReBarUEFI 问题列表：

```
site:github.com/xCuri0/ReBarUEFI <主板型号>
```

对于您的 P100 / M40 / RTX 3090 实验，重要的 BIOS 项为：

```
高级
 └─ PCI 子系统设置
      ├─ Above 4G Decoding
      ├─ Re-Size BAR Support
      ├─ MMIO High Base
      ├─ MMIO High Size

启动
 └─ CSM
      └─ 禁用
```

对于较老的平台（X79/X99/Z77/Z97），**MMIO 空间通常比可见的 4G 选项更重要**，尤其对于显存 24GB+ 的 GPU。ReBarUEFI 指出，HEDT/服务器主板可能需要调整 `MMIOH Size` / `MMIO High Granularity Size` 以适应大显存 GPU。（[GitHub][4]）

参考资料：

* [xCuri0/ReBarUEFI GitHub](https://github.com/xCuri0/ReBarUEFI?utm_source=chatgpt.com)
* [ReBarUEFI Wiki - 常见问题](https://github.com/xCuri0/ReBarUEFI/wiki/Common-issues-%28and-fixes%29?utm_source=chatgpt.com)

[1]: https://github.com/xCuri0/ReBarUEFI/wiki/Enabling-hidden-4G-decoding?utm_source=chatgpt.com "启用隐藏的 4G 解码 · xCuri0/ReBarUEFI Wiki · GitHub"
[2]: https://github.com/xCuri0/ReBarUEFI/blob/master/README.md?plain=1&utm_source=chatgpt.com "ReBarUEFI/README.md at master · xCuri0/ReBarUEFI · GitHub"
[3]: https://github.com/xCuri0/ReBarUEFI/wiki?utm_source=chatgpt.com "首页 · xCuri0/ReBarUEFI Wiki · GitHub"
[4]: https://github.com/xCuri0/ReBarUEFI/wiki/Common-issues-%28and-fixes%29?utm_source=chatgpt.com "常见问题（及修复）· xCuri0/ReBarUEFI Wiki · GitHub"