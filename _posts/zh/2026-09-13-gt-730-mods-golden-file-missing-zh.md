---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GT 730 MODS金色文件缺失
translated: true
type: note
---

**问题：** 在测试 GT 730 GPU 时，MODS 为何失败？

**答案：**

从图 3 可清晰看到错误信息：

```
Failed to open file gldGK208S.bin – No such file or directory
Error 0000000000011 : Global.LoadGoldenValuesHelper file does not exist
Error Code = 0000000000011 (file does not exist)
```

### 根本原因

MODS 正在为您的 GPU 寻找一个名为 `gldGK208S.bin` 的 **Golden Values 文件**。从图 2 可知，GPU 设备 ID 为 `GK208S`（GT 730 使用 GK208 芯片）。该 `.bin` 文件包含针对该特定 GPU 芯片的参考/基线测试值，但 **您的 MODS 安装中缺少该文件**。

### 原因分析

| 原因 | 详情 |
| --- | --- |
| **MODS 版本过新** | MODS 455.127 可能已移除对旧版 Kepler (GK208) 黄金值文件的支持 |
| **MODS 包不完整** | `gldGK208S.bin` 从未被包含或被删除 |
| **错误的 MODS 构建** | 部分 MODS 构建仅针对特定 GPU 系列 |

### 解决方法

1. **获取正确的 MODS 包**，该包需包含 Kepler GPU 支持——较旧的 MODS 版本（R450 之前）更可靠地包含 GK208 黄金值文件
2. **手动获取 `gldGK208S.bin`** 来自 NVIDIA，并将其放置在 MODS 工作目录中
3. **使用 `-skipGoldenCheck` 标志运行 MODS**，如果只想进行功能测试而不进行黄金值比较：

   ```bash
   ./mods gputest.js --skipGoldenCheck
   ```

4. **联系 NVIDIA**——MODS 是内部/合作伙伴工具；GK208S 黄金值文件可能需要直接请求

### 硬件说明

GT 730 (GK208) 是 **Kepler 架构 GPU（2014 年）**。较新驱动分支（如 r455）中对旧版 Kepler 的 MODS 支持可能有限。

---

参考文献：

- [NVIDIA MODS Overview](https://developer.nvidia.com/mods)
- [GK208 / GT 730 Architecture Info](https://www.techpowerup.com/gpu-specs/nvidia-gk208b.g186)
