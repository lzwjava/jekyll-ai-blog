---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Windows 安装过程中缺少驱动程序的问题
translated: true
type: note
---

**Question:** 为什么我在 Lenovo Xiaoxin 14 IAH8 上安装 Windows 时，即使解压了 .exe 文件，在 FAT32 USB 闪存盘上仍然找不到驱动程序？

**Answer:**

这是在 Xiaoxin 14 IAH8 等现代 Lenovo 笔记本电脑（使用 Intel 13/14 代或类似的 Alder Lake/Raptor Lake 硬件）上安装 Windows 时，加载存储驱动程序（特别是 Intel RST/IRST 或 VMD）非常常见的问题。当你点击 **Load driver** → **Browse** 时，“什么都没有显示”或没有出现驱动程序通常是因为以下原因：

### 最可能的原因及修复方法（分步指南）

1. **文件夹结构错误或 .inf 文件埋得太深**
   当你解压 Lenovo/Intel 的 .exe 驱动程序包时（使用 7-Zip 或右键“全部解压缩”），实际的 .inf 文件通常位于子文件夹中，例如：
   - `RST` / `VMD` / `f6flpy-x64` / `Production` / `Win64` 等。
   Windows 安装程序 **只扫描你选择的文件夹** 及其直接子文件夹——它不会自动深度挖掘。

   **修复方法：**
   - 在另一台电脑上，完全解压 .exe 文件。
   - 寻找包含 `.inf` 文件的文件夹（特别是名为 `iaStorAC.inf`, `iaAHCIC.inf`, `VMD.inf`, `iaStorVD.inf` 或类似的文件）。
   - 将 **仅包含这些 .inf 文件的文件夹**（或者仅仅是 .inf + .sys/.cat 文件）直接复制到 FAT32 USB 的根目录（或命名为 `Drivers` 或 `IRST` 的简单文件夹中）。
   - 避免嵌套太多子文件夹（例如，不要路径设置为 `USB:\SomeLongPath\Sub\Sub\inf`）。
   - 在安装期间：Browse → 选择 USB 驱动器 → 打开包含 .inf 文件的确切文件夹 → Windows 现在应该列出匹配的驱动程序 → 选择一个（通常是 RST 或 VMD 变体）→ OK。

2. **BIOS 中启用了 Intel VMD (Volume Management Device) —— 这会隐藏驱动器，除非使用 VMD 专用驱动程序**
   许多第 12 代及以上的 Intel Lenovo 笔记本电脑默认 **启用 VMD**（用于 RAID/Optane 支持），如果不加载正确的 VMD 驱动程序，NVMe SSD 将不可见。标准的 RST 驱动程序在此处通常会失效。

   **最佳且最简单的修复方法（推荐大多数用户使用）：**
   - 重启 → 进入 BIOS（通常在出现 Lenovo 标志期间反复按 **F2** 或 **Fn+F2**）。
   - 转到 **Configuration** 或 **Advanced** 选项卡。
   - 找到 **Intel VMD controller**（或 **VMD Setup Menu**, **Intel Volume Management Device**）。
   - 将其 **Disable**（设置为 Disabled）。
   - 同时检查 **Storage Mode** / **SATA Configuration** → 设置为 **AHCI**（不要用 RAID 或 Intel RST Premium）。
   - 保存并退出（F10 → Yes）。
   - 重新启动到 Windows USB 安装程序 → 此时 SSD 应该会在 **不加载任何驱动程序** 的情况下出现！
   （这是进行 Windows 纯净安装最简单的解决方案——如果你以后需要 RAID，你会失去它，但大多数家庭用户并不需要。）

3. **下载了错误的驱动程序版本**
   - Lenovo 官网针对 IdeaPad Slim 3 14IAH8 可能不再列出专门的 "F6"（floppy 驱动）包——现在很多都是纯 .exe 文件。
   - 尝试直接从 Intel 下载 **最新的 Intel RST 驱动程序**（针对 13/14 代的 19.x 或 20.x 版本）：
     下载地址 → <https://www.intel.com/content/www/us/en/download/720755/intel-rapid-storage-technology-driver-installation-software-with-intel-optane-memory.html> （或搜索 "Intel RST VMD driver"）。
     解压 → 寻找 VMD 文件夹或 f6flpy-x64 等效文件夹。

4. **USB 问题或 Windows 安装程序的怪癖**
   - 如果有 **USB 2.0 端口**，请确保将 FAT32 USB 插入其中（某些安装程序在启动初期会忽略 USB 3.0）。
   - 尝试更换另一个 USB 闪存盘（某些廉价盘存在兼容性问题）。
   - 确保 Windows ISO 是最新的（如果太旧，请使用 Rufus 或 Microsoft 官方工具重新制作）。

### 快速总结表 – 优先尝试的操作

| 步骤 | 操作 | 为什么有效 |
| ------ | -------- | -------------- |
| 1 | 在 BIOS 中禁用 Intel VMD + 设置 AHCI | 绕过对特殊驱动的需求 — 驱动器原生显示 |
| 2 | 解压 .exe → 仅将包含 .inf 的文件夹复制到 USB 根目录 | Windows 现在可以识别驱动文件 |
| 3 | 使用 Intel 官方最新的 RST/VMD 驱动程序包 | Lenovo 的驱动可能过时或不匹配 |
| 4 | 首先检查 BIOS 是否能识别 SSD | 确认硬件正常 |

安装完成后，可从 Lenovo Vantage 或支持网站安装完整的驱动程序。如果之前禁用了 VMD，以后有需要可以重新启用它（但需重新安装 RST 软件）。

以上操作应该能让你的驱动器显示出来——在类似的 Lenovo 机型中，通过 BIOS 更改设置可以解决 80% 以上的此类案例。

**References:**

- [https://www.youtube.com/watch?v=Sp2AYnGfIOk](https://www.youtube.com/watch?v=Sp2AYnGfIOk)
- [https://www.dell.com/support/kbdoc/en-mq/000188116](https://www.dell.com/support/kbdoc/en-mq/000188116)
- [https://www.intel.com/content/www/us/en/support/articles/000092508/technologies.html](https://www.intel.com/content/www/us/en/support/articles/000092508/technologies.html)
- [https://forums.lenovo.com/t5/ThinkBook-Laptops/Windows-installation-does-not-see-my-hard-drive/m-p/5212595](https://forums.lenovo.com/t5/ThinkBook-Laptops/Windows-installation-does-not-see-my-hard-drive/m-p/5212595)
- [https://www.reddit.com/r/intel/comments/1762sj6/intel_rst_vmd_driver_is_now_an_exe_and_not](https://www.reddit.com/r/intel/comments/1762sj6/intel_rst_vmd_driver_is_now_an_exe_and_not)
