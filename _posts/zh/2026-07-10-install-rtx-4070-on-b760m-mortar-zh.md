---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在B760M迫击炮上安装RTX 4070
translated: true
type: note
---

问题：如何将 MSI GeForce RTX 4070 显卡物理安装到 MSI MAG B760M Mortar 主板上？这两个组件分别是什么？

回答：

## 这两个部件是什么

**MSI MAG B760M Mortar** — 一款 micro-ATX 主板，Intel B760 芯片组，LGA1700 插槽（支持第12/13代 Core、Pentium Gold、Celeron）。与显卡安装相关的特性：它带有一个 PCIe 5.0/4.0/3.0 x16 插槽，配有钢制装甲加固，顶部插槽经过强化，通过 CPU 连接，支持最高 PCIe 5.0 x16 速度；而第二个全长插槽通过芯片组连接，仅支持 PCIe 4.0 x4。因此，你只有一个真正的 x16 电气插槽——那就是你需要安装显卡的位置。

**MSI GeForce RTX 4070** — Ada Lovelace GPU，12GB GDDR6X，PCIe Gen4 接口。根据你购买的 SKU（Gaming X Trio、Ventus 等），功耗和连接器略有不同。Gaming X Trio 12G 版本：功耗 215W，16-pin 电源连接器，建议 PSU 650W，显卡尺寸 338 x 141 x 52 mm。该 16-pin 连接器为 12VHPWR/12V-2x6 类型——你的 PSU 要么有原生的 12VHPWR 线缆，要么显卡附带一个适配器，可连接来自 PSU 的 2-3 个 8-pin PCIe 接口。

## 物理安装步骤

1. **关闭电源并拔掉 PSU 插头。** 接地（触摸机箱外壳，或佩戴防静电腕带）。

2. **找到正确的插槽。** 在 B760M Mortar 上，使用 `PCI_E1`——顶部、连接 CPU 且带有金属“钢制装甲”护罩的 x16 插槽。不要使用底部连接芯片组的插槽；它在电气上仅支持 x4，会严重限制 RTX 4070 的性能。

3. **卸下机箱后部对应显卡高度的 I/O 挡板**（RTX 4070 通常为三槽卡，因此卸下 2-3 个挡片）。

4. **打开 PCIe 插槽末端的卡扣**（强化卡扣——MSI 的“加宽 PCI-E 卡扣”设计便于徒手插拔）。

5. **对齐并插入显卡。** 将显卡的 PCIe 金手指与插槽对齐，保持显卡水平，均匀用力从两端垂直向下按压，直到听到/感觉到卡扣咔哒一声闭合，显卡与插槽完全贴合。

6. **用螺丝将显卡挡板固定到机箱后部**（根据占用槽位数量，通常需要 1-2 颗螺丝）。

7. **连接电源线。** 如果 PSU 是 ATX 3.0/3.1 原生支持，则直接插入 16-pin 12VHPWR 线缆；否则使用附带的适配器，将 PSU 的 2-3 个 8-pin PCIe 线缆连接到适配器，再将适配器的单一 16-pin 插头插入显卡。确保**完全插紧**——半插入的 12VHPWR 连接器是已知的故障模式（导致熔化），已有大量报告。

8. **检查物理支撑。** 显卡长度 338mm，重量约 1.2kg，请确认机箱有足够空间，并考虑使用显卡支撑支架/防下垂支架，因为 micro-ATX 机箱有时显卡间隙较短——如果尚未购买，请先测量。

9. **开机，进入 BIOS（按 Del 键），确认显卡已检测到**（在 PCIe 设备列表中），然后启动进入操作系统。

10. **驱动安装。** 在 Linux 上（假设你的工作站支持 Ubuntu）：通过 `ubuntu-drivers devices` 然后 `sudo ubuntu-drivers autoinstall` 安装 NVIDIA 专有驱动，或者直接获取 CUDA 工具包（如果你想在这张卡上运行训练任务）：

```bash
# Ubuntu — 检查推荐驱动
ubuntu-drivers devices

# 安装
sudo ubuntu-drivers autoinstall
sudo reboot

# 验证
nvidia-smi
```

## 值得注意的一点（针对你的设备）

你的 192.168.1.36 工作站已经列出了 RTX 4070 12GB——如果这是该机器的*第二块*显卡或升级件，请检查你的 PSU 余量，考虑其他设备（CPU、其他 GPU 等）的功耗。RTX 4070 的最低要求是 3 个 8-pin PCIe 连接器或一条 450W 容量的 PCIe Gen5 电源线，但 MSI 对 Gaming X Trio 的建议是 650W——不同板卡合作伙伴推荐的 PSU 功率不同，因此务必查阅你具体型号的规格表。

参考：

- [MSI MAG B760M Mortar WIFI 评测 — Tom's Hardware](https://www.tomshardware.com/reviews/msi-mag-b760m-mortar-wifi-review)
- [MSI MAG B760M MORTAR WIFI — Newegg 规格表](https://www.newegg.com/msi-mag-b760m-mortar-wifi-micro-atx-motherboard-intel-b760-lga-1700/p/N82E16813144586)
- [MSI GeForce RTX 4070 GAMING X TRIO 12G 规格](https://www.msi.com/Graphics-Card/GeForce-RTX-4070-GAMING-X-TRIO-12G/Specification)
- [Corsair — 最适合 RTX 4070 的 PSU 是什么](https://www.corsair.com/us/en/explorer/diy-builder/power-supply-units/what-psu-is-best-for-rtx-4070/)