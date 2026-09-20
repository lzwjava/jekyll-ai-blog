---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M40 BAR分析修正
translated: true
type: note
---

问题：**“这是M40 / BAR / Above-4G分析正确吗？”**

答案：**大部分正确，但有两个重要修正。**

1. **`BAR1 [size=16M]` *并不*意味着M40仅暴露了其24 GB显存中的16 MB。**  
   这是PCIe BAR映射，而非物理显存容量。M40确实拥有**24 GB GDDR5显存**。

2. **关于Resizable BAR的说法过于绝对。**  
   Tesla M40/GM200不提供现代意义上的Resizable BAR支持（即Ampere时代GPU所具备的功能）。因此，您不应期望M40上有一个24 GB的可调整BAR。但说*“Resizable BAR是随RTX 30 / Ampere引入的”*在历史上过于简化：PCIe Resizable BAR能力早于Ampere存在；Ampere是NVIDIA将其作为消费级显眼功能推出的时代。

3. **Above 4G Decoding是24 GB M40的重要BIOS设置。**  
   这涉及主机PCIe MMIO地址空间，而非直接关乎GPU是否物理具有24 GB。对于大型GPU BAR，固件需要能够分配4 GB边界以上的PCIe MMIO空间。在现代化服务器/工作站上，**通常应启用Above 4G Decoding**。

4. **关于NVIDIA驱动程序的陈述略有误导。**  
   驱动程序无法神奇地克服固件资源分配失败。大致顺序如下：

   ```text
   M40
     │
     ├── 24 GB物理显存
     │
     ├── PCIe BAR
     │     ├── BAR0：寄存器/控制
     │     └── BAR1：显存窗口/映射
     │
     ▼
   PCIe固件资源分配
     │
     ├── 32位MMIO空间
     └── 64位MMIO空间（>4 GB）
     │
     ▼
   Linux PCI子系统
     │
     ▼
   NVIDIA驱动程序
   ```

   您当前看到的：

   ```text
   内存位于 f1000000（32位，非预取）[大小=16M]
   ```

   **不足以得出结论说24 GB显存被错误映射。**

### 我建议检查的事项

运行：

```bash
sudo lspci -vv -s <M40_BDF>
```

以及：

```bash
sudo lspci -vvv -s <M40_BDF> | grep -E \
  '内存位于|预取|区域|LnkCap|LnkSta|Resizable BAR|物理插槽'
```

另外：

```bash
nvidia-smi
```

在驱动加载后执行。

对于MMIO问题最有用的检查：

```bash
sudo dmesg | grep -Ei 'pci|bar|mmio|resource|nvidia'
```

如果M40健康，`nvidia-smi`最终应报告类似内容：

```text
内存使用
0MiB / 24576MiB
```

（或驱动程序占用的少量内存）。

### 一个微妙的要点

**`lspci`显示的16 MB BAR1不一定意味着BAR1永久限制为16 MB的显存访问。** Maxwell Tesla卡使用相对较小的BAR窗口，驱动程序可以管理对更大显存空间的映射。因此，不要将：

```text
BAR1 = 16M
```

作为M40无法访问其全部24 GB的证据。

更有效的测试是：

```bash
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv
```

如果报告的大约**24576 MiB总内存**，则无论`lspci`显示16 MB BAR，全部显存都可用。

**底线：** 所引用的分析给出了正确的操作建议——**如果BIOS提供，请启用Above 4G Decoding**——但关于24 GB M40*需要*巨大BAR来寻址所有显存的解释是不正确/过于简化的。单独的16 MB BAR1输出本身不是问题。

我还可以逐行分析实际的`lspci -vv`输出，以确定您的M40的PCIe/MMIO配置是否健康。