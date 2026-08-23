---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 恢复不良VBIOS后的CMP 170HX
translated: true
type: note
---

**一块能识别但刷坏 VBIOS 后无法安装驱动的 CMP 170HX 8GB 能修好吗？**

答案：

是的，**很可能可以恢复**，因为以下症状：

> "能认卡, 驱动打不上"
> "刷了vbios就驱动认不了"
> "默认坏卡出售"

通常意味着 GPU 芯片是完好的，PCIe 枚举正常，但 **VBIOS/固件状态无效**。

对于 CMP 170HX，随意刷写 VBIOS 尤其危险。这张卡不是普通的 GeForce 卡。网上很多"解锁 PCIe 4.0 / A100 BIOS"的教程都是错误或不完整的。已知的解锁路径**不需要刷写 VBIOS**；它是通过驱动端的运行时补丁完成的。（[GitHub][1]）

## 恢复路径

### 1. 首先检查 GPU 是否仍可见

启动进入 Linux：

```bash
lspci -nn | grep -i nvidia
```

预期输出：

```
NVIDIA Corporation Device 20c2
```

对于 CMP 170HX 8GB，PCI ID 通常是：

```
10de:20c2
```

（[GitHub][2]）

然后执行：

```bash
lspci -vv -s <GPU_BUS>
```

如果 PCIe 能看到它，说明 GPU 核心很可能没问题。

---

## 2. 先转储当前 VBIOS

在操作任何东西之前：

```bash
sudo nvflash --save backup.rom
```

如果 nvflash 无法访问，可以尝试：

* 使用另一块正常工作的 NVIDIA 卡作为主显示卡
* Linux
* SPI 编程器（CH341A）作为最后手段

CMP 170HX 的恢复通常需要外部 SPI 闪存编程器，如果 ROM 区域已损坏。（[GitHub][1]）

---

## 3. 刷写正确的 CMP 170HX 官方 ROM

你需要**精确的 8GB ROM**，而不是：

* A100 BIOS ❌
* 10GB CMP 170HX BIOS ❌
* 随便找的矿卡 BIOS ❌

已知的 8GB CMP 170HX VBIOS 示例：

```
92.00.67.00.01
92.00.6D.00.0A
```

（[GitHub][2]）

刷写：

```bash
sudo nvflash -6 stock_170hx_8gb.rom
```

如果 nvflash 拒绝：

```bash
sudo nvflash --protectoff
sudo nvflash -6 stock_170hx_8gb.rom
```

---

## 4. 如果 nvflash 提示固件不匹配

由于 CMP 卡有安全校验，软件刷写可能会失败。

这时可以：

### SPI 编程器方法

硬件准备：

```
CH341A
SOIC8 夹子
备份 ROM
```

步骤：

1. 拆卸散热器
2. 找到 SPI 闪存芯片
3. 读取原 ROM
4. 写入干净 ROM
5. 校验
6. 开机

社区文档也指出，外部 SPI 是 VBIOS 刷坏后的可靠恢复路径。（[GitHub][1]）

---

## 5. 恢复后，不要为了解锁而刷 BIOS

对于 CMP 170HX 8GB：

更安全的路径：

```
官方 VBIOS
        |
        v
Linux
        |
        v
打过补丁的 NVIDIA 驱动
        |
        v
64GB 解锁
```

已知的解锁方式修改的是运行时驱动/GSP 行为，不涉及 VBIOS 刷写。（[GitHub][3]）

---

## 快速诊断表

| 症状                              | 含义                           | 解决方法           |
| ------------------------------- | ------------------------------ | ------------------ |
| `lspci` 能识别 GPU，驱动失败      | VBIOS 不匹配/损坏               | 恢复官方 ROM        |
| 无 PCIe 设备                     | 硬件损坏或供电问题             | 检查电路板          |
| nvflash 可以读写                 | 容易恢复                       | 刷写正确的 ROM      |
| nvflash 被阻止                   | 安全锁                         | SPI 编程器          |
| 风扇转但驱动不认                 | 固件初始化失败                 | ROM 恢复            |

根据你的描述，我的猜测：

> "一开始是好的，乱刷 VBIOS 后坏"

= **90% 的可能性只是 VBIOS 刷错了，不是 GPU 损坏**。

关键问题是：

1. `lspci -nn` 显示什么？
2. `nvidia-smi` 报什么错误？
3. `nvflash --save backup.rom` 能否读取当前 BIOS？

这三个输出决定了是软件恢复还是 SPI 恢复。

[1]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/hardware/vbios.md?utm_source=chatgpt.com "cmp170hx/docs/hardware/vbios.md at main · Consensus-Protocol/cmp170hx · GitHub"
[2]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/start/identify-your-card.md?utm_source=chatgpt.com "cmp170hx/docs/start/identify-your-card.md at main · Consensus-Protocol/cmp170hx · GitHub"
[3]: https://github.com/Consensus-Protocol/cmp170hx/blob/main/docs/unlock/overview.md?utm_source=chatgpt.com "cmp170hx/docs/unlock/overview.md at main · Consensus-Protocol/cmp170hx · GitHub"