---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MODS GPU版本兼容性
translated: true
type: note
---

问得好。以下是文档中关于 MODS 版本兼容性的说明：

## MODS 版本与 GPU 支持

### MODS R367（本文档 - 2015 年 7 月）
根据文档明确提及的内容，该版本支持最高至 **Kepler** 和 **早期 Maxwell** 的 GPU 架构：

| GPU 家族 | 架构 | 示例 | R367 是否支持？ |
|---|---|---|---|
| **Fermi** | GF1xx | GTX 480, 580 | ✅ 是 |
| **Kepler** | GK1xx | **GTX 760**, GTX 680, GT 710 | ✅ 是 |
| **Maxwell**（早期） | GM1xx | GTX 750 Ti, GTX 960 | ✅ 部分支持 |
| **Maxwell**（后期） | GM2xx | GTX 980, GTX 970 | ⚠️ 可能（边缘支持） |
| **Pascal** | GP1xx | GTX 1060, 1070, 1080 | ❌ 否 |
| **Turing** | TU1xx | RTX 2060, 2070, 2080 | ❌ 否 |
| **Ampere** | GA1xx | **RTX 3060**, RTX 3070, 3080 | ❌ 否 |

### 针对您的具体 GPU：

**GTX 760（Kepler，2013）** — ✅ 应与 MODS R367 配合使用
- 它是 Kepler GK104 芯片，文档明确支持该芯片，并提供诸如 `-gpu_family kepler` 等标志，同时提到“在 Kepler GPU 上测试 InlineToMemory 类”

**RTX 3060（Ampere，2021）** — ❌ **将无法与 MODS R367 配合使用**
- MODS R367 发布时距 RTX 3060 上市约早 6 年
- Ampere 架构于 2020 年推出，比该 MODS 版本晚了五年
- 您需要更新的 MODS 版本（R4xx 或 R5xx 系列）

### 如果找不到设备：

**1. 检查是否需要更新的 MODS 版本**
```bash
mods -v   # 显示版本号，如 "367.XX"
```
对于 RTX 3060，您可能需要 **R495 或更新版本** 的 MODS（与支持 Ampere 的驱动分支匹配）。

**2. 检查 NVIDIA 显示驱动是否干扰**
```
请务必确保 nvidia 内核模块未加载，
否则系统可能变得不稳定。
```
文档明确警告：*“请务必确保 nvidia 内核模块未加载”* — 如果 Xorg 或 NVIDIA 驱动正在运行，MODS 可能无法检测到 GPU。

**3. 尝试架构特定标志**
```bash
mods gputest.js -mfg -gpu_family kepler     # 用于 GTX 760
mods gputest.js -mfg -gpu_family fermi      # 用于较旧的 GPU
```

**4. 检查错误代码**
- 错误 **31**：“系统中找到的唯一设备已过时” — MODS 识别到 GPU，但 GPU 太旧
- 错误 **710**：“选中的设备不受支持” — 对于该 MODS 版本，GPU 太新
- 错误 **“NVRM card not present”** — GPU 可能完全未被检测到

### 总结
- **GTX 760 → 使用 MODS R367**（此版本即可）
- **RTX 3060 → 需要 MODS R495 或更新版本**（R367 太旧）