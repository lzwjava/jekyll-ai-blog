---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Windows 安装程序缺少 NVMe 驱动程序
translated: true
type: note
---

**Question:** 为什么在 Lenovo Xiaoxin 14 IAH8 安装过程中，插入存有这些提取出的 Lenovo 驱动 .exe 文件（如 chipset-KZSC030FLWDYANE0.exe, intelVGA-KZSG0A0FT22GJNE0.exe 等）的 FAT32 USB 闪存盘，Windows 却找不到/无法加载任何驱动程序？

**Answer:**

主要问题在于**你列出的所有 .exe 文件**（来自 ~/Downloads/driver）都不包含 Windows 安装过程中识别 SSD 所需的 **storage/NVMe/Intel RST/VMD 驱动程序**。这些文件是用于其他硬件的：

- chipset-KZSC030FLWDYANE0.exe → Chipset 驱动（安装后使用）
- intelVGA-KZSG0A0FT22GJNE0.exe → Intel Graphics 显卡驱动
- audio-KZSA050F2QF1NNE0.exe → Audio 音频驱动
- camera-KZSD040FAVJPUNE0.exe → Camera 摄像头驱动
- fingerprint-KZSD030F36UBVNE0.exe → Fingerprint 指纹驱动
- RTKwlan-KZSW060F0H46SNE0.exe → WiFi (Realtek) 无线网卡驱动
- 等等。

这些都不是 **Intel Rapid Storage Technology (IRST/RST)** 或 **VMD** 驱动包，无法提供在“加载驱动程序”步骤中（当 SSD 不可见时）所需的 .inf 文件（如 iaStorAC.inf, iaStorVD.inf 或 VMD.inf）。

### 为什么浏览 USB 时什么都没有显示

即使你将这些 .exe 文件复制到了 FAT32 USB：
- Windows 安装程序**无法运行 .exe 安装包** —— 它只能识别原始驱动文件（.inf + .sys + .cat）。
- 你必须先（在另一台电脑上）**提取**正确的 RST .exe，找到包含 .inf 文件的子文件夹（通常在 `f6flpy-x64`, `VMD`, `Production`, 或 `Win64` 中），然后**只将该文件夹**（或其内容）复制到 USB 根目录或简单的文件夹（如 `\IRST`）中。
- 你目前的文件中没有这些存储相关的 .inf 文件，因此浏览时显示没有兼容的驱动 → “未发现驱动程序”或列表为空。

### 推荐的修复方法：两条路径（任选其一）

**路径 1：最简单且最可靠 —— 在 BIOS 中禁用 VMD（无需驱动程序）**
- 重启笔记本 → 在出现 Lenovo 标志时反复按 **F2** (或 Fn+F2) 进入 BIOS。
- 前往 **Configuration** 选项卡（或 **Advanced** / **Device Configuration**）。
- 查找以下选项：
  - **Intel VMD controller** / **VMD Setup Menu** / **Intel Volume Management Device** → 设置为 **Disabled**。
  - **SATA Controller Mode** / **Storage Mode** → 设置为 **AHCI** (不要选 RAID 或 RST)。
- **F10** → Save & Exit → Yes。
- 重新从 Windows USB 安装盘启动 → SSD 现在应该会自动出现在驱动器列表中（不再需要“加载驱动程序”）。
- 这是因为 VMD 会在标准 Windows 安装程序中隐藏 NVMe SSD，除非加载了专门的 VMD 驱动程序。禁用它会使用原生 AHCI/NVMe 模式（对大多数用户来说足够，除非你需要 RAID）。

**路径 2：保持 VMD 开启 —— 加载正确的 RST/VMD 驱动程序**
1. 在另一台 Windows 电脑上，下载**最新的 Intel RST 驱动程序**（包含对 13 代/14 代处理器的 VMD 支持）：
   - 来自 Intel 官网：https://www.intel.com/content/www/us/en/download/720755/intel-rapid-storage-technology-driver-installation-software-with-intel-optane-memory.html (或搜索 "Intel RST driver VMD")。
   - 或来自 Lenovo 全球支持站对应 IdeaPad Slim 3 14IAH8 (等效机型)：在 https://pcsupport.lenovo.com 搜索 "IdeaPad Slim 3 14IAH8" → Drivers → Storage → Intel Rapid Storage Technology。
2. 使用命令运行 .exe 进行提取（在下载文件夹中打开 Command Prompt）：
   ```
   SetupRST.exe -extractdrivers C:\ExtractedRST
   ```
   (如果 -extractdrivers 不起作用，请尝试使用 7-Zip 提取。)
3. 在提取后的文件夹中，找到包含 .inf 文件的子文件夹 (例如 `f6flpy-x64`, `VMD`, `Drivers\VMD`)。
   - 常见文件：iaStorVD.inf, iaStorAC.inf, VMD.inf。
4. 将整个子文件夹（或仅 inf/.sys/.cat 文件）复制到 FAT32 USB 根目录 (例如 USB:\VMD\ 或 USB:\IRST\\)。
5. 在 Windows 安装过程中：
   - 在“你想将 Windows 安装在哪里？”界面 → **加载驱动程序** → **浏览** → 选择 USB → 打开包含 .inf 的文件夹 → 选择匹配的驱动程序（尝试 VMD 或 RST 变体）→ 确定。
   - 加载后 SSD 应该会显示出来。

安装完成后（无论采用哪种路径），请运行 Lenovo Vantage + Windows Update 获取全套驱动（包括你已经有的那些）。

建议**先尝试路径 1** —— 对于 2023/2024 年推出的搭载 Intel 13 代/14 代处理器的 Lenovo IdeaPad/Slim 机型，在 BIOS 中禁用即可立即解决此问题。

**参考资料：**

- [https://www.youtube.com/watch?v=Sp2AYnGfIOk](https://www.youtube.com/watch?v=Sp2AYnGfIOk)
- [https://www.intel.com/content/www/us/en/support/articles/000092508/technologies.html](https://www.intel.com/content/www/us/en/support/articles/000092508/technologies.html)
- [https://www.youtube.com/watch?v=41C71-dvv-4](https://www.youtube.com/watch?v=41C71-dvv-4)
- [https://www.reddit.com/r/intel/comments/1762sj6/intel_rst_vmd_driver_is_now_an_exe_and_not](https://www.reddit.com/r/intel/comments/1762sj6/intel_rst_vmd_driver_is_now_an_exe_and_not)
- [https://support.lenovo.com/us/en/solutions/ht506197-nvme-ssd-pci-device-will-be-invisible-when-intel-vmd-is-enabled-lenovo-thinksystem](https://support.lenovo.com/us/en/solutions/ht506197-nvme-ssd-pci-device-will-be-invisible-when-intel-vmd-is-enabled-lenovo-thinksystem)
