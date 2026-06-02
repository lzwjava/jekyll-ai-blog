---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 光纤连接器类型指南
translated: true
type: note
---

Question: 对于 fiber optic cables，LC-LC、SC-SC 等表示什么意思？

Answer:

**LC-LC**、**SC-SC** 及类似的表示方法用于描述 **fiber optic patch cables**（也称为 jumper cables），通过指定每一端的 **connector types** 来命名。

- **LC-LC** 表示电缆两端都有一个 **LC connector**。
- **SC-SC** 表示电缆两端都有一个 **SC connector**。
- 其他常见示例包括 **LC-SC**（一端为 LC，另一端为 SC）、**ST-ST**、**FC-FC**、**MTP-MTP** 等。

这些是 networking、data centers、telecom 和 fiber-to-the-home 安装中最广泛使用的 **duplex**（双纤）patch cords 类型。

### LC 和 SC 代表什么？

- **LC** → **Lucent Connector**（也称为 Little Connector 或 Local Connector）
  - 使用较小的 **1.25 mm** 陶瓷 ferrule。
  - 尺寸非常紧凑（约为 SC 占用空间的一半）。
  - 使用小锁扣（latch clip）固定（类似于 RJ45 夹子）。
  - 在现代高密度环境中占主导地位，如 data centers、SFP/SFP+/QSFP transceivers 以及高速 switches/routers。

- **SC** → **Subscriber Connector**（也称为 Square Connector 或 Standard Connector）
  - 使用较大的 **2.5 mm** 陶瓷 ferrule。
  - 方形主体，带有 push-pull 机制和锁定片。
  - 在旧款 telecom 设备、PON networks（GPON/EPON）、有线电视以及 1990s–2010s 期间的许多 enterprise 安装中非常常见。

### LC 与 SC 的快速比较

| Feature              | LC Connector                  | SC Connector                  |
|----------------------|-------------------------------|-------------------------------|
| Ferrule diameter     | 1.25 mm                       | 2.5 mm                        |
| Size / footprint     | Small / high-density          | Larger                        |
| Latching mechanism   | Small latch clip              | Push-pull with tab            |
| Typical use today    | Data centers, 10G/25G/40G/100G+ | Telecom, PON, older equipment |
| Density in panels    | Higher (more ports per space) | Lower                         |
| Insertion / durability | Good, but smaller latch       | Very robust, easy to handle   |

LC 和 SC 都能提供卓越的光学性能（low insertion loss 和 high return loss），并且都可以用于 **single-mode** 或 **multi-mode** fiber。

### 你可能看到的其他常见标记

- **LC-SC** → Hybrid cable（一端 LC，一端 SC）——通常用于将新设备连接到旧的基础设施。
- **LC-LC Duplex** → 指定为双芯光纤（最常见的 patch cable 样式）。
- **LC/UPC-LC/UPC** → 增加了 polish 类型（UPC = Ultra Physical Contact，最常见；APC = Angled Physical Contact，用于某些 single-mode 应用中以降低反射）。

简而言之：**LC-LC** = 两端都是小型现代 LC connectors；**SC-SC** = 两端都是较大的经典 SC connectors。

References:

- [Fiber Optic Connector Types Explained | FiberCablesDirect](https://fibercablesdirect.com/content/23-fiber-optic-connector-types-explained)
- [LC vs SC Connectors: Which to Choose? - VCELINK](https://www.vcelink.com/blogs/focus/lc-vs-sc-connectors)
- [Comparing SC and LC Fibre Optic Connectors | iTel Networks](https://itel.com/blog/comparing-sc-and-lc-fibre-optic-connectors)
- [Fiber-optic connectors: SC vs. LC | Arrow.com](https://www.arrow.com/en/research-and-events/articles/fiber-optic-connectors-sc-vs-lc)
