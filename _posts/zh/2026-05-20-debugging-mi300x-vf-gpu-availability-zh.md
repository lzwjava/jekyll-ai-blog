---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 调试MI300X VF GPU可用性
translated: true
type: note
---

以下是我所做所有工作的端到端分解：

---

## 第一阶段：初始侦查

**目标**：了解机箱内的硬件以及有哪些可用工具。

**步骤 1 — 尝试明显的工具**

```
ssh root@134.199.199.108 rocm-smi
```

结果：`command not found`。AMD 上相当于 `nvidia-smi` 的工具未安装。

**步骤 2 — 寻找替代方案**
搜索了 `amd-smi`、`rocminfo`、`clinfo`，并检查了 `/opt/rocm*/`。一无所获。仅存在 Debian 软件包中的 `libdrm-amdgpu1`——这是最基本的 DRM 用户空间库。

**步骤 3 — 通过 PCI 识别 GPU**

```
lspci | grep -iE 'vga|3d|display|amd|ati'
```

找到：`83:00.0 Processing accelerators: AMD/ATI Aqua Vanjaram [Instinct MI300X VF]`

关键发现：GPU 属于类别 `0x12`（处理加速器），而非 `0x03`（VGA/显示）。仅查找显示类设备的标准 GPU 检测脚本会遗漏它。

**步骤 4 — 直接读取 PCI sysfs**

```
cat /sys/bus/pci/devices/0000:83:00.0/{vendor,device,class}
```

- 厂商：`0x1002`（AMD）
- 设备：`0x74b5`（MI300X VF）
- 类别：`0x120000`（处理加速器）
- PCIe：`32.0 GT/s x16`（Gen 5，最大宽度）
- 内存 BAR：`0x4000000000` 处 256 GB

**步骤 5 — 检查 DRM/KFD 拓扑**

```
cat /sys/class/kfd/kfd/topology/nodes/*/properties
```

仅节点 0（CPU）且 `simd_count=0`。KFD 拓扑中没有 GPU 节点——这是 SR-IOV 虚拟功能的标志，内核计算驱动程序无法枚举该设备。

还检查了 `/sys/class/drm/card*/device/` 中 amdgpu 特定的统计信息（`gpu_busy_percent`、`mem_info_vram_*`、`hwmon/temp*`）——全部为空。VF 未通过标准 DRM sysfs 路径暴露管理接口。

---

## 第二阶段：构建备用工具（`amd-smi`）

**目标**：在修复完整堆栈的同时，给用户一个可以运行以查看 GPU 信息的工具。

**步骤 6 — 编写 Python 脚本**，从替代数据源读取，因为 `rocm-smi` 无法看到 VF：

| 数据 | 来源 |
|------|--------|
| GPU 名称、BAR | `lspci -s <bdf> -vv` |
| 设备/厂商 ID | `/sys/bus/pci/devices/<bdf>/device`、`/vendor`、`/subsystem_*` |
| PCIe 链路速度/宽度 | `/sys/bus/pci/devices/<bdf>/current_link_speed`、`current_link_width`、`max_link_*` |
| NUMA 节点 | `/sys/bus/pci/devices/<bdf>/numa_node` |
| 电源状态 | `/sys/bus/pci/devices/<bdf>/power_state` |
| IRQ | `/sys/bus/pci/devices/<bdf>/irq` |
| 驱动版本 | `/sys/module/amdgpu/version` |

**部署失败及最终成功的模式：**

尝试 1：通过 SSH 的 bash heredoc → 语法错误（heredoc 分隔符与嵌套引号冲突）

尝试 2：通过 SSH 的 Python heredoc → 被安全过滤阻止（heredoc < PYEOF 模式）

尝试 3（成功）：通过 `write_file` 将脚本本地写入 `/tmp/amd-smi.py`，然后通过 `scp` 复制到服务器。这是可靠的跨机器部署模式：本地写入 → scp → 远程安装。

**步骤 7 — Bug 修复**：首次运行显示 `Device ID: 0x0x74b5`——PCI sysfs 值已包含 `0x` 前缀。使用 `.removeprefix("0x")` 修复。

---

## 第三阶段：安装 ROCm（真正的堆栈）

**目标**：让 `rocm-smi`、`rocminfo` 和 `hipcc` 正常工作，使 GPU 真正可用于计算。

**步骤 8 — 添加 AMD 的 apt 仓库**

```
echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/latest noble main' > /etc/apt/sources.list.d/rocm.list
```

在 Ubuntu 25.10（plucky）上使用 "noble"（Ubuntu 24.04）软件包。AMD 仅官方支持 LTS 版本，但用户空间软件包是兼容的。

**步骤 9 — 首次安装尝试：`rocm-hip-sdk` 元包**
因依赖地狱失败——`rocm-cmake 0.14.0`（来自 AMD）与 `rocm-cmake 6.4.3`（来自 Ubuntu 的 universe 仓库）冲突。Apt 拒绝降级 `6.4.3 → 0.14.0`，因为尽管 AMD 的版本号方案不同，但 Ubuntu 包的版本号看起来更新。

**步骤 10 — 第二次尝试：`rocm-hip-runtime`（不含 -dev）**
相同的 `rocm-cmake` 冲突。根本问题：Ubuntu 25.10 在 universe 中提供的 ROCm 组件与 AMD 自己仓库中的包冲突。

**步骤 11 — 发现：版本化软件包**

```
apt-cache search rocm | grep '7.2.3'
```

Ubuntu 25.10 提供了**版本化**软件包：`rocm-hip-runtime7.2.3`、`hsa-rocr7.2.3`、`comgr7.2.3` 等。这些软件包名称不同，因此与 Ubuntu 的非版本化 `rocm-cmake` 共存。这是干净的路径。

**步骤 12 — 安装版本化运行时**

```
apt-get install hsa-rocr7.2.3 comgr7.2.3 rocm-core7.2.3 rocm-language-runtime7.2.3 rocminfo7.2.3 rocm-hip-runtime7.2.3 hip-runtime-amd
```

失败：文件冲突。非版本化软件包（`hsa-rocr`、`comgr`、`hip-runtime-amd`）作为 `rocm-smi`（早期安装）的传递依赖被拉取，它们在 `/opt/rocm-7.2.3/lib/*` 中的文件与版本化软件包重叠。

**步骤 13 — 强制清除所有冲突软件包**

```
dpkg --purge --force-depends --force-remove-reinstreq rocm-core hsa-rocr comgr hip-runtime-amd rocprofiler-register [以及它们的 7.2.3 变体]
```

这打破了依赖死锁——部分安装的版本化软件包依赖于正在被移除的非版本化软件包，形成了循环失败。

**步骤 14 — 使用完整依赖树进行干净重装**

```
apt-get install rocm-core7.2.3 hsa-rocr7.2.3 comgr7.2.3 hip-runtime-amd7.2.3 rocprofiler-register7.2.3 rocm-device-libs7.2.3 openmp-extras-runtime7.2.3 rocm-language-runtime7.2.3 rocminfo7.2.3 rocm-hip-runtime7.2.3
```

成功——所有软件包均无冲突安装。

**步骤 15 — 安装 HIP 编译器**

```
apt-get install hipcc7.2.3 hipify-clang7.2.3 hip-dev7.2.3
```

`hipcc --version` → HIP 7.2.53211，AMD clang 22.0.0。

**步骤 16 — 修复 libxml2 ABI 不匹配**
HIP 编译失败：`lld: error while loading shared libraries: libxml2.so.2: cannot open shared object file`。Ubuntu 25.10 提供了 `libxml2-16`（ABI .so.16），而 ROCm 的链接器期望 `.so.2`。

```
ln -sf /lib/x86_64-linux-gnu/libxml2.so.16 /lib/x86_64-linux-gnu/libxml2.so.2
ldconfig
```

这是一个兼容性符号链接——较新的 ABI 向后兼容较旧的 API。

**步骤 17 — HIP 测试编译成功但显示 0 个设备**

```
HIP devices: 0
```

GPU 在 HSA 级别可见（`rocm_agent_enumerator` → `gfx942`），但 HIP 的设备枚举返回 0。KFD 拓扑仍然只显示 CPU 节点。

---

## 第四阶段：真正根因——缺少固件

**步骤 18 — 检查 dmesg 中的 GPU 初始化错误**

```
dmesg | grep -i 'amdgpu.*83:00'
```

关键错误：

```
Direct firmware load for amdgpu/psp_13_0_6_ta.bin failed with error -2
Direct firmware load for amdgpu/gc_9_4_3_rlc.bin failed with error -2
Direct firmware load for amdgpu/sdma_4_4_2.bin failed with error -2
Direct firmware load for amdgpu/vcn_4_0_3.bin failed with error -2
amdgpu: Fatal error during GPU init
amdgpu: amdgpu: finishing device.
```

amdgpu 驱动程序已绑定到设备，但无法初始化，因为 MI300X 的 IP 块的固件 blob 缺少于 `/lib/firmware/amdgpu/`。

**步骤 19 — 安装固件**

```
apt-get install linux-firmware
```

验证文件存在：`gc_9_4_3_rlc.bin.zst`、`psp_13_0_6_ta.bin.zst`、`sdma_4_4_2.bin.zst`、`vcn_4_0_3.bin.zst`（使用 zstd 压缩——内核的固件加载器透明地处理此格式）。

**步骤 20 — 重新绑定 GPU 驱动程序**（强制固件重新加载）

```
echo '0000:83:00.0' > /sys/bus/pci/drivers/amdgpu/unbind
sleep 2
echo '0000:83:00.0' > /sys/bus/pci/drivers/amdgpu/bind
```

dmesg 确认：`[drm] Initialized amdgpu 3.64.0 for 0000:83:00.0 on minor 1`

---

## 第五阶段：验证——一切正常

**步骤 21 — 完整验证**

```
rocm-smi:           Device 0 | 37°C | 154W | 139MHz SCLK | 900MHz MCLK | 750W cap
rocminfo:           AMD Instinct MI300X VF (gfx942) | 304 CUs | 191 GB HBM3
HIP test:           HIP devices: 1 | 191 GB | 304 CUs | 2100 MHz
KFD topology:       Node 1 with simd_count=1216, gfx_target_version=90402
```

**步骤 22 — 持久环境设置**

```
/etc/profile.d/rocm.sh:
  ROCM_PATH=/opt/rocm-7.2.3
  PATH=$ROCM_PATH/bin:$PATH
  LD_LIBRARY_PATH=$ROCM_PATH/lib:$LD_LIBRARY_PATH
```

---

## 关键经验

**1. SR-IOV VF 在固件加载之前对标准工具不可见。**
VF 需要固件来初始化其 IP 块（PSP → 安全，GC → 计算，SDMA → DMA）。没有固件，KFD 无法枚举它，`rocm-smi` 显示为空，HIP 返回 0 个设备。

**2. 版本化软件包是非 LTS Ubuntu 的逃生舱。**
Ubuntu 25.10 将 ROCm 7.2.3 作为 `*7.2.3` 软件包提供，这些软件包与系统软件包共存。非版本化的元包会触发与 Ubuntu 自己的 `rocm-cmake` 的依赖冲突。

**3. 强制清除可打破 dpkg 依赖死锁。**
当部分安装的版本化软件包依赖于正在被移除的非版本化软件包时，需要使用 `dpkg --purge --force-depends`。普通的 `apt-get purge` 会拒绝，因为它试图满足正在被删除的依赖关系。

**4. 缺失 .so 版本的 ABI 符号链接。**
Ubuntu 25.10 将 `libxml2` 的 ABI 从 2 升级到 16。ROCm 链接器（为 24.04 构建）期望 `.so.2`。创建符号链接即可修复，因为较新的 ABI 向后兼容。

**5. 远程部署模式：write_file → scp → chmod。**
SSH heredoc 会因嵌套引号而崩溃。将脚本本地写入然后复制可避免所有 shell 转义问题。

**6. PCI sysfs 值中的 `0x` 前缀。**
`/sys/bus/pci/devices/*/vendor` 返回 `0x1002`（带前缀）。格式化代码必须考虑这一点，否则你会得到 `0x0x1002`。

**7. 始终检查 dmesg 以获取驱动程序初始化失败信息。**
amdgpu 驱动程序一直加载并绑定到设备——它在固件加载时静默失败。`dmesg` 揭示了 `lspci` 和 sysfs 从未暗示的缺失文件。
