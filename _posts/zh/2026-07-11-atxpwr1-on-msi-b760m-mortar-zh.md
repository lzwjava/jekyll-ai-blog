---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI B760M MORTAR上的ATX_PWR1
translated: true
type: note
---

问题：微星MAG B760M MORTAR WIFI主板上的ATX_PWR1接口是什么意思？

回答：

`ATX_PWR1` 是主板上的**主24针ATX电源接口**——从电源向主板（芯片组、内存、I/O、PCIe插槽、风扇等）供电的主要输入端。它与 `CPU_PWR1`/`CPU_PWR2` 接口（位于CPU插座附近的8+8针EPS12V接口，直接为VRM/CPU供电）不同。

在这块主板上：

- CPU_PWR1~2 和 ATX_PWR1 是电源接口，允许您连接ATX电源。
- CPU_PWR1/2 各为8针，为CPU供电提供 `+12V` 和 `地线` 引脚。
- ATX_PWR1 是24针接口，引脚1为 `+3.3V`（ATX_PWR1 引脚1信号名称1 +3.3V），其余引脚遵循标准ATX24针引脚定义（+5V、+12V、PS_ON、PWR_OK等——在我找到的摘录中，手册只显示了引脚1-2，但它是标准的24针ATX规范）。

**物理位置**：它位于主板右侧边缘，靠近内存插槽——在组件总览图中，它位于JUSB3、JUSB4和PUMP_FAN1附近，紧邻您所期望的24针边缘接口。

**实际装机时**：将电源的24针线缆插入 `ATX_PWR1`，将8针（如果您使用高端CPU，则为双8针）EPS线缆插入 `CPU_PWR1`（以及 `CPU_PWR2` 如果有的话）。如果要在安装CPU/内存之前通过Flash BIOS按钮更新BIOS，微星的说明确认您只需将电源连接到CPU_PWR1和ATX_PWR1——此步骤不需要CPU或内存，这在您希望在完成装机前更新BIOS（例如确保新CPU第一天就得到支持）时非常方便。

参考资料：

- [MSI MAG B760M MORTAR WIFI II 用户指南 (PDF)](https://download-2.msi.com/archive/mnu_exe/mb/MAGB760MMORTARII_MAGB760MMORTARWIFIII_EN.pdf)
- [MSI MAG B760M MORTAR WIFI II 手册 (manua.ls)](https://www.manua.ls/msi/mag-b760m-mortar-wifi-ii/manual)
- [MSI MAG B760M MORTAR WIFI 产品页面](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI)