---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ATX_PWR1 在微星 B760M 迫击炮上
translated: true
type: note
---

**问题：MSI MAG B760M Mortar WiFi 主板上的 ATX_PWR1 是什么？**

**回答：**

`ATX_PWR1` 是电源（PSU）连接到主板的 **24-pin 主电源接口**，负责为主板供电。([MSI][1])

物理外观：

```
PSU 24-pin ATX 线缆
        |
        v

+----------------+
| ATX_PWR1       |
| [24 针]        |
+----------------+

主板
```

你的 PSU 通常会有一根标有以下字样的线缆：

```
ATX 24P
MB
MAIN
```

将其插入 `ATX_PWR1`。

它提供以下电压：

* +3.3V → 芯片组、内存逻辑、PCIe 设备
* +5V → USB、控制器、存储设备
* +12V → 主板电源轨道
* 待机电源 (5VSB) → 支持主板唤醒功能

MSI MAG B760M Mortar WiFi 主板具有以下电源接口：

* `ATX_PWR1` = 24-pin 主板供电
* `CPU_PWR1` + `CPU_PWR2` = 8-pin CPU EPS 电源接口 ([MSI 下载][2])

布局大致如下：

```
主板顶部

[ CPU 插槽 ]

[ CPU_PWR1 ][ CPU_PWR2 ]
    8-pin      8-pin

中部：

[ PCIe GPU 插槽 ]

右侧边缘：

[ ATX_PWR1 ]
[  24-pin  ]
```

对于你的装机配置：

* RTX 4070 / MI50 GPU → 由 PSU 单独供电
* CPU → CPU_PWR1（如果 CPU 功耗高则连接 CPU_PWR2）
* 主板 → ATX_PWR1

对于常规 CPU，如 i5-12400 / i5-13600 / i7（默认频率）：

* 连接 **ATX_PWR1**
* 连接 **CPU_PWR1**
* CPU_PWR2 通常为可选，除非是重负载或高端 CPU。MSI 在该主板上设计了双 8-pin CPU 接口，以支持更高功耗的 CPU。([MSI][3])

所以基本连接如下：

```
PSU
 |
 +-- 24 pin ATX  ----------> ATX_PWR1
 |
 +-- 8 pin EPS CPU --------> CPU_PWR1
 |
 +-- 另一个 8 pin EPS -----> CPU_PWR2（可选）
 |
 +-- PCIe 电源 -----------> GPU
```

对于你的 MI50 AI 工作站装机，最重要的是：**确保你的 PSU 有足够的 PCIe/EPS 接口和额定功率。ATX_PWR1 本身是标准接口，所有 ATX PSU 都配备此接口。**

[1]: https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/Specification?utm_source=chatgpt.com "MAG B760M MORTAR WIFI"
[2]: https://download-2.msi.com/archive/mnu_exe/mb/B760MMORTAR_WIFI_MAXWIFI.pdf?utm_source=chatgpt.com "MAG B760M MORTAR MAX WIFI"
[3]: https://us.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/Overview?utm_source=chatgpt.com "MAG B760M MORTAR WIFI"