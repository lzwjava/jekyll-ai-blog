---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 需要ATX 12V连接器
translated: true
type: note
---

**问题：** 主板上的 ATX 12V 接口有什么用途？是否必须插上？

**解答：**

**ATX 12V 的用途：**

4 针 ATX 12V 接口专门为 CPU 提供 12V 供电。它连接至 VRM（电压调节模块），VRM 再将电压降至 CPU 运行所需的精确水平。如果没有它，即使插上了 24 针主电源接口，CPU 也无法获得电力。

**是否需要插上？**

**是的——绝对必要。** 如果忘记连接 4 针 ATX 12V 电源插头，系统将无法启动。

以下是两个主要电源接口的简要说明：

| 接口 | 针脚数 | 供电对象 |
|---|---|---|
| EATXPWR | 24 针 | 主板、内存、PCIe 插槽、存储设备 |
| ATX12V | 4 针 | 仅 CPU（通过 VRM） |

**未插 ATX 12V 时的常见症状：**
- 系统通电（风扇转动、LED 亮起）但**无自检 / 无显示**
- 按下电源后立即关机
- 持续重启循环

对于 H81M-K，华硕建议使用符合 ATX 12V 规范 2.0 的电源供应器（PSU），额定功率至少 300W。

简而言之——**切勿遗漏**。它和 24 针接口同样重要。

---

**参考资料：**
- [华硕 H81M-K 用户手册 – ATX 电源接口（第 25 页）](https://www.manualslib.com/manual/565354/Asus-H81m-K.html?page=25)
- [华硕 H81M-K 布局内容（第 12 页）](https://www.manualowl.com/m/Asus/H81M-K/Manual/372249?page=12)